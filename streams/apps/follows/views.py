from django.http import Http404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from streams.apps.streams.models import Stream
from rest_framework.views import Response
from rest_framework import status
from .models import Follow
from .serializers import FollowSerializer
from streams.apps.accounts.serializers import AccountSerializer
from streams.apps.accounts.models import Account
from streams.apps.profiles.models import Profile
from streams.apps.profiles.serializers import ProfileSerializer
from streams.apps.streams.models import Stream


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
#     # TODO: Can I do this on one query? Is this one query?
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
#     # TODO: These calls could probably be cleaner.
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
