from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import StreamSerializer
from .models import Stream
from streams.apps.follows.models import Follow
from streams.apps.posts.models import Post
from streams.apps.posts.serializers import PostSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_stream(request):
    serializer_context = {'account': request.user}
    serializer = StreamSerializer(data=request.data, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_stream(request, stream_id):
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404

    if stream.owner != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = StreamSerializer(stream)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def read_public_stream(request, stream_id):
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404

    if stream.is_private:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = StreamSerializer(stream)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def read_public_streams_for(request, handle):
    try:
        streams = Stream.objects.filter(owner__handle=handle, is_private=False)
    except Stream.DoesNotExist:
        raise Http404

    serializer = StreamSerializer(streams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_stream(request, stream_id):
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404

    if stream.owner != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = StreamSerializer(stream, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stream(request, stream_id):
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404

    if stream.owner != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    stream.set_deleted()
    return Response({'Deleted': f'{stream}'}, status=status.HTTP_204_NO_CONTENT)






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_my_own_streams(request):
    streams = Stream.objects.filter(owner=request.user)
    serializer = StreamSerializer(streams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_streams_i_follow(request):
    stream_ids = Follow.objects.filter(account=request.user, stream_follows_account=True).values('stream')
    streams = Stream.objects.filter(id__in=stream_ids)
    serializer = StreamSerializer(streams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_posts_for_stream(request):
    try:
        stream_id = request.data['stream_id']
    except KeyError:
        return Response({'details': {'required fields': ['stream_id']}}, status=status.HTTP_400_BAD_REQUEST)

    post_ids = Follow.objects.filter(stream__id=stream_id, stream_follows_account=True).values('account__posts')
    posts = Post.objects.filter(id__in=post_ids)

    paginator = PageNumberPagination()
    paginator.page_size = 3
    result_page = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
