from django.http import Http404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from streams.apps.streams.models import Stream
from rest_framework.views import Response
from rest_framework import status
from itertools import chain
from django.db import IntegrityError
from django.db.models import Q
from .models import ProfileFollow, StreamFollow
from .serializers import ProfileFollowSerializer, StreamFollowSerializer
from rest_framework.pagination import PageNumberPagination

from streams.apps.profiles.models import Profile
from streams.apps.follows.models import ProfileFollow
from streams.apps.profiles.serializers import ProfileSerializer
from streams.apps.streams.serializers import StreamSerializer
from streams.apps.streams.models import Stream


def get_followers_for_profile_helper(handle, request):
    # get the streams that follow this profile, then get their owners.
    streams_following = ProfileFollow.objects.filter(profile__account__handle=handle).values('stream')
    profile_owners_of_streams_following = Stream.objects.filter(pk__in=streams_following).values('owner')

    # get all the people following any one of these streams that is following this profile.
    profiles_following_streams_following = StreamFollow.objects.filter(stream__in=streams_following)\
        .values('profile')

    profiles = Profile.objects\
        .filter(Q(pk__in=profile_owners_of_streams_following) | Q(pk__in=profiles_following_streams_following)).distinct()

    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(profiles, request)

    serializer = ProfileSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_followers_for_profile(request):
    handle = request.data.get('handle')
    if not handle:
        return Response({'details': {'required_fields': ['handle']}}, status=status.HTTP_400_BAD_REQUEST)
    return get_followers_for_profile_helper(handle, request)
    # return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_followers_for_me(request):
    return get_followers_for_profile_helper(request.user.handle, request)


def get_following_for_profile_helper(handle, request):
    stream_ids = Stream.objects.filter(owner__account__handle=handle)
    profiles_ids = ProfileFollow.objects.filter(stream__in=stream_ids).values('profile').distinct()

    stream_follow_ids = StreamFollow.objects.filter(profile__account__handle=handle).values('stream')
    followed_streams = Stream.objects.filter(pk__in=stream_follow_ids)
    followed_stream_profiles_followed_ids = ProfileFollow.objects\
        .filter(stream__in=followed_streams).values('profile').distinct()

    profiles = Profile.objects\
        .filter(Q(pk__in=profiles_ids) | Q(pk__in=followed_stream_profiles_followed_ids)).distinct()

    paginator = PageNumberPagination()
    paginator.page_size = 3
    result_page = paginator.paginate_queryset(profiles, request)

    serializer = ProfileSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_following_for_profile(request):
    handle = request.data.get('handle')
    if not handle:
        return Response({'details': {'required_fields': ['profileId']}}, status=status.HTTP_400_BAD_REQUEST)
    return get_following_for_profile_helper(handle, request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_following_for_me(request):
    return get_following_for_profile_helper(request.user.handle, request)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_profile_from_profile(request):
    """
    This will un-follow a profile from a profile.  So from any and all streams,
    and un-following streams themselves which follow the profile.
    """
    profile_id = request.data.get('profileId')
    if not profile_id:
        return Response({'details': {'required_fields': ['profileId']}}, status=status.HTTP_400_BAD_REQUEST)

    my_stream_ids = Stream.objects.filter(owner=request.user.profile)
    profile_follows = ProfileFollow.objects.filter(stream__in=my_stream_ids, profile=profile_id)

    for follow in profile_follows:
        follow.set_deleted()

    stream_follows = StreamFollow.objects.filter(profile=request.user.profile)

    for follow in stream_follows:
        """
        if this stream you are following follows the profile you are trying to unfollow,
        then un-follow this stream.
        """
        try:
            ProfileFollow.objects.get(stream=follow.stream.id, profile=profile_id)
        except ProfileFollow.DoesNotExist:
            pass
        else:
            follow.set_deleted()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_stream(request):
    """
    un-follow a stream you are following.
    """
    stream_id = request.data.get('streamId')
    if not stream_id:
        return Response({'details': {'required_fields': ['streamId']}}, status=status.HTTP_400_BAD_REQUEST)

    try:
        follow = StreamFollow.objects.get(profile=request.user.profile, stream=stream_id)
    except StreamFollow.DoesNotExist:
        raise Http404

    follow.set_deleted()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_profile(request):
    stream_id = request.data.get('streamId')
    handle = request.data.get('handle')
    if not stream_id or not handle:
        return Response({'details': {'required_fields': ['streamId', 'profileId']}}, status=status.HTTP_400_BAD_REQUEST)

    try:
        stream = Stream.objects.get(pk=stream_id)
        profile = Profile.objects.get(account__handle=handle)
    except Stream.DoesNotExist:
        raise Http404
    except Profile.DoesNotExist:
        raise Http404

    if stream.owner.id is not request.user.profile.id:
        print(stream.owner)
        print(request.user.profile)
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        profile_follow = ProfileFollow.objects.get(stream=stream.id, profile=profile.id)
    except ProfileFollow.DoesNotExist:
        raise Http404

    profile_follow.set_deleted()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_profile(request):
    try:
        handle = request.data['handle']
        stream_id = request.data['streamId']
        profile = Profile.objects.get(account__handle=handle)
        stream = Stream.objects.get(pk=stream_id)
    except KeyError:
        return Response({'details': {'required fields': ['handle', 'streamId']}}, status=status.HTTP_400_BAD_REQUEST)
    except Stream.DoesNotExist:
        raise Http404('Stream with that id not found.')
    except Profile.DoesNotExist:
        raise Http404('Profile with that id not found.')

    if stream.owner.id != request.user.profile.id:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer_context = {'profile': profile, 'stream': stream}
    serializer = ProfileFollowSerializer(data={}, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    try:
        serializer.save()
    except IntegrityError as e:
        return Response(status=status.HTTP_200_OK)

    # profile_serializer = ProfileSerializer(profile)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_stream(request):
    try:
        stream_id = request.data['streamId']
        stream = Stream.objects.get(pk=stream_id)
    except KeyError:
        return Response({'details': {'required fields': ['streamId']}}, status=status.HTTP_400_BAD_REQUEST)
    except Stream.DoesNotExist:
        raise Http404('Stream with that id not found.')

    serializer_context = {'stream': stream, 'profile': request.user.profile}
    serializer = StreamFollowSerializer(data={}, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    stream_serializer = StreamSerializer(stream)
    return Response(stream_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_followers_for_stream(request):
    stream_id = request.data.get('streamId')
    if not stream_id:
        return Response({'details': {'required_fields': ['streamId']}}, status=status.HTTP_400_BAD_REQUEST)

    profile_ids = StreamFollow.objects.filter(stream=stream_id).values('profile')
    profiles = Profile.objects.filter(pk__in=profile_ids)

    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(profiles, request)

    serializer = ProfileSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_following_for_stream(request):
    stream_id = request.data.get('streamId')
    if not stream_id:
        return Response({'details': {'required_fields': ['streamId']}}, status=status.HTTP_400_BAD_REQUEST)

    profile_ids = ProfileFollow.objects.filter(stream=stream_id).values('profile')
    profiles = Profile.objects.filter(pk__in=profile_ids)

    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(profiles, request)

    serializer = ProfileSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def follow_stream(request, stream_id):
#     try:
#         stream = Stream.objects.get(pk=stream_id, is_private=False)
#     except Stream.DoesNotExist:
#         raise Http404
#
#     data = {'stream_follows_account': False}
#     serializer_context = {'account': request.user, 'stream': stream}
#     serializer = FollowSerializer(data=data, context=serializer_context)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def follow_account(request):
#     handle = request.data.get('handle')
#     stream_id = request.data.get('stream_id')
#     if not handle and not stream_id:
#         return Response({'error': 'Missing required fields: handle, stream_id'}, status=status.HTTP_400_BAD_REQUEST)
#     if not handle:
#         return Response({'Missing required field': 'handle'}, status=status.HTTP_400_BAD_REQUEST)
#     if not stream_id:
#         return Response({'Missing required field': 'stream_id'}, status=status.HTTP_400_BAD_REQUEST)
#
#     try:
#         account = Account.objects.get(handle=handle)
#     except Account.DoesNotExist:
#         raise Http404('Account with that handle not found.')
#
#     try:
#         stream = Stream.objects.get(pk=stream_id)
#     except Stream.DoesNotExist:
#         raise Http404('Stream with that id not found.')
#
#     # We can't let someone follow a stream for someone else.
#     if stream.owner != request.user:
#         print(stream)
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     data = {'stream_follows_account': True}
#     serializer_context = {'account': account, 'stream': stream}
#     serializer = FollowSerializer(data=data, context=serializer_context)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_accounts_following_stream(request, stream_id):
#     try:
#         stream = Stream.objects.get(pk=stream_id)
#     except Stream.DoesNotExist:
#         raise Http404
#
#     account_ids = Follow.objects.filter(stream__id=stream_id, stream_follows_account=False).values('account')
#     accounts = Account.objects.filter(id__in=account_ids)
#     # if not accounts:
#     #     raise Http404
#     serializer = AccountSerializer(accounts, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_accounts_followed_by_stream(request, stream_id):
#     # Grab stream and check to see if it is private, and then restrict access if it is.
#     try:
#         stream = Stream.objects.get(pk=stream_id)
#     except Stream.DoesNotExist:
#         raise Http404
#
#     if stream.is_private and (stream.owner != request.user):
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     account_ids = Follow.objects.filter(stream__id=stream_id, stream_follows_account=True).values('account')
#     profiles = Profile.objects.filter(account_id__in=account_ids)
#     serializer = ProfileSerializer(profiles, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_accounts_followed_by_account(request, handle):
#     # First we have to get the streams the account owns and follows,
#     # then get everyone those streams follow, and then filter out duplicates.
#
#     # Get the account for the handle
#     try:
#         account = Account.objects.get(handle=handle)
#     except Account.DoesNotExist:
#         raise Http404
#
#     # Get the stream ids for ones the account owns
#     own_stream_ids = Stream.objects.filter(owner=account).values('id')
#
#     # Get the streams the account follows.
#     following_stream_ids = Follow.objects.filter(account=account, stream_follows_account=False).values('stream')
#
#     # Get the profiles for the stream_ids
#     # Duplicates are filtered since you can own and follow streams that follow the same people,
#     # but they should not be listed as two follows.
#     profiles = Profile.objects.filter(account__streams__id__in=own_stream_ids).distinct()
#     profiles = profiles | Profile.objects.filter(account__streams__id__in=following_stream_ids).distinct()
#     serializer = ProfileSerializer(profiles, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_accounts_following_account(request, handle):
#     # First we have to get the account from the handle.
#     try:
#         account = Account.objects.get(handle=handle)
#     except Account.DoesNotExist:
#         assert Http404
#     print(account)
#     # Next we have to get all profiles of streams following that account
#     profile_ids = Follow.objects.filter(account=account, stream_follows_account=True).values('stream__owner__profile')
#     print(profile_ids)
#     # Now that we have the profile ids, let's grab the profiles.
#     # Some people will have multiples streams that follow the same account, so filter out duplicates.
#     profiles = Profile.objects.filter(id__in=profile_ids).distinct()
#     serializer = ProfileSerializer(profiles, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
