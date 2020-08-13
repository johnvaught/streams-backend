from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .serializers import StreamSerializer
from .models import Stream
from streams.apps.profiles.models import Profile
from streams.apps.follows.models import ProfileFollow, StreamFollow
from streams.apps.follows.serializers import ProfileFollowSerializer
from streams.apps.posts.models import Post
from streams.apps.posts.serializers import PostSerializer


# def get_streams_for_profile_helper(profile):
#     followed_streams = StreamFollow.objects.filter(profile=profile).values('stream')
#     all_streams = Stream.objects.filter(Q(owner=profile) | Q(pk__in=followed_streams))
#     streams_serializer = StreamSerializer(all_streams, many=True)
#
#     posts = {}
#     for stream in streams_serializer.data:
#         profile_ids = ProfileFollow.objects.filter(stream=stream['id']).values('profile')
#         stream_posts = Post.objects.filter(owner__in=profile_ids).order_by('-id')[:20]
#
#         paginator = PageNumberPagination(stream_posts)
#         post_serializer = PostSerializer(stream_posts, many=True)
#         posts[stream['id']] = post_serializer.data
#
#     return {'streams': streams_serializer.data, 'posts': posts, 'profileId': profile.id}


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def get_streams(request):
#     data = get_streams_for_profile_helper(request.user.profile)
#     return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_streams_for_profile(request):
    profile_id = request.data.get('profileId')
    if not profile_id:
        return Response({'details': {'required_fields': ['profileId']}}, status=status.HTTP_400_BAD_REQUEST)
    try:
        profile = Profile.objects.get(pk=profile_id)
    except Profile.DoesNotExist:
        raise Http404

    followed_streams = StreamFollow.objects.filter(profile=profile).values('stream')
    all_streams = Stream.objects.filter(Q(owner=profile) | Q(pk__in=followed_streams))
    streams_serializer = StreamSerializer(all_streams, many=True)

    posts = {}
    for stream in streams_serializer.data:
        profile_ids = ProfileFollow.objects.filter(stream=stream['id']).values('profile')
        stream_posts = Post.objects.filter(owner__in=profile_ids).order_by('-id')[:20]

        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(stream_posts, request)

        post_serializer = PostSerializer(result_page, many=True)
        posts[stream['id']] = post_serializer.data

    data = {'streams': streams_serializer.data, 'posts': posts, 'profileId': profile.id}

    return Response(data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def follow_profile(request):
#     try:
#         profile_id = request.data['profileId']
#         stream_id = request.data['streamId']
#         profile = Profile.objects.get(pk=profile_id)
#         stream = Stream.objects.get(pk=stream_id)
#     except KeyError:
#         return Response({'details': {'required fields': ['profileId', 'streamId']}}, status=status.HTTP_400_BAD_REQUEST)
#     except Stream.DoesNotExist:
#         raise Http404('Stream with that id not found.')
#     except Profile.DoesNotExist:
#         raise Http404('Profile with that id not found.')
#
#     serializer_context = {'profile': profile, 'stream': stream}
#     serializer = ProfileFollowSerializer(data={}, context=serializer_context)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#
#     return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_stream(request):
#     serializer_context = {'account': request.user}
#     serializer = StreamSerializer(data=request.data, context=serializer_context)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def read_stream(request, stream_id):
#     try:
#         stream = Stream.objects.get(pk=stream_id)
#     except Stream.DoesNotExist:
#         raise Http404
#
#     if stream.owner != request.user:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     serializer = StreamSerializer(stream)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def read_public_stream(request, stream_id):
#     try:
#         stream = Stream.objects.get(pk=stream_id)
#     except Stream.DoesNotExist:
#         raise Http404
#
#     if stream.is_private:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     serializer = StreamSerializer(stream)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def read_public_streams_for(request, handle):
#     try:
#         streams = Stream.objects.filter(owner__handle=handle, is_private=False)
#     except Stream.DoesNotExist:
#         raise Http404
#
#     serializer = StreamSerializer(streams, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_stream(request, stream_id):
#     try:
#         stream = Stream.objects.get(pk=stream_id)
#     except Stream.DoesNotExist:
#         raise Http404
#
#     if stream.owner != request.user:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     serializer = StreamSerializer(stream, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_stream(request, stream_id):
#     try:
#         stream = Stream.objects.get(pk=stream_id)
#     except Stream.DoesNotExist:
#         raise Http404
#
#     if stream.owner != request.user:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     stream.set_deleted()
#     return Response({'Deleted': f'{stream}'}, status=status.HTTP_204_NO_CONTENT)
#

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def get_my_own_streams(request):
#     streams = Stream.objects.filter(owner=request.user)
#     serializer = StreamSerializer(streams, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def get_streams_i_follow(request):
#     stream_ids = Follow.objects.filter(account=request.user, stream_follows_account=True).values('stream')
#     streams = Stream.objects.filter(id__in=stream_ids)
#     serializer = StreamSerializer(streams, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def get_posts_for_stream(request):
#     try:
#         stream_id = request.data['stream_id']
#     except KeyError:
#         return Response({'details': {'required fields': ['stream_id']}}, status=status.HTTP_400_BAD_REQUEST)
#
#     post_ids = Follow.objects.filter(stream__id=stream_id, stream_follows_account=True).values('account__posts')
#     posts = Post.objects.filter(id__in=post_ids)
#
#     paginator = PageNumberPagination()
#     paginator.page_size = 9
#     result_page = paginator.paginate_queryset(posts, request)
#
#     serializer = PostSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)
