from django.http import Http404
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from streams.apps.follows.models import ProfileFollow
from streams.apps.streams.models import Stream
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


@api_view(['POST'])
@permission_classes([AllowAny])
def get_post(request):
    post_id = request.data.get('postId')
    if not post_id:
        return Response({'details': {'required_fields': ['postId']}}, status=status.HTTP_400_BAD_REQUEST)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404

    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_posts_for_profile(request):
    handle = request.data.get('handle')
    if not handle:
        return Response({'details': {'required_fields': ['handle']}}, status=status.HTTP_400_BAD_REQUEST)

    posts = Post.objects.filter(owner__account__handle=handle)

    paginator = LimitOffsetPagination()
    paginator.default_limit = 6
    result_page = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_posts_for_stream(request):
    stream_id = request.data.get('streamId')
    if not stream_id:
        return Response({'details': {'required_fields': ['streamId']}}, status=status.HTTP_400_BAD_REQUEST)
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404
    except ValidationError:
        return Response({'details': {'required field as UUID': ['streamId']}}, status=status.HTTP_400_BAD_REQUEST)

    profiles = ProfileFollow.objects.filter(stream=stream.id).values('profile')
    posts = Post.objects.filter(owner__in=profiles)

    paginator = LimitOffsetPagination()
    paginator.default_limit = 12
    result_page = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_explore(request):
    posts = Post.objects.all()

    paginator = LimitOffsetPagination()
    paginator.default_limit = 6
    result_page = paginator.paginate_queryset(posts, request)

    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_post(request):
#     serializer_context = {'account': request.user}
#     serializer = PostSerializer(data=request.data, context=serializer_context)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def read_public_post(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         raise Http404
#
#     if post.account.profile.is_private:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     serializer = PostSerializer(post)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def read_public_posts_for(request, handle):
#     since_date = request.query_params.get('since')
#     print(since_date)
#     if since_date:
#         posts = Post.objects.filter(account__handle=handle, created_at__gt=since_date)
#     else:
#         posts = Post.objects.filter(account__handle=handle)
#     print(posts)
#     serializer = PostSerializer(posts, many=True)
#     print(serializer.data)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_post(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         raise Http404
#
#     if post.account != request.user:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     serializer = PostSerializer(post, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_post(request, post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         raise Http404
#
#     """
#     Object level permissions classes not supported for function based views.
#     https://github.com/encode/django-rest-framework/issues/1697
#     Workaround below.
#     """
#     if post.account != request.user:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     post.set_deleted()
#     return Response({'Deleted': f'{post}'}, status=status.HTTP_204_NO_CONTENT)

#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def get_posts(request):
#     posts = Post.objects.filter(account__handle=request.user.handle)
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def get_my_posts(request):
#     print('called')
#     posts = Post.objects.filter(account__handle=request.user.handle)
#     print('here')
#
#     paginator = PageNumberPagination()
#     paginator.page_size = 3
#     result_page = paginator.paginate_queryset(posts, request)
#
#     serializer = PostSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)
