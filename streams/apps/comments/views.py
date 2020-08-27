from django.http import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from streams.apps.posts.models import Post
from .serlializers import PostCommentSerializer
from .models import PostComment
# from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.views.decorators.csrf import csrf_exempt

from streams.apps.core.pagination import LimitOffsetPaginationTime
from datetime import datetime

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post_comment(request):
    post_id = request.data.get('postId')
    comment_data = request.data.get('comment')
    if not post_id:
        print('no post id??')
        return Response({'details': {'required_fields': ['postId']}}, status=status.HTTP_400_BAD_REQUEST)
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404

    comment_id = comment_data.pop('id')
    serializer_context = {'id': comment_id, 'post': post, 'owner': request.user.profile}
    serializer = PostCommentSerializer(data=comment_data, context=serializer_context)

    # serializer = PostCommentSerializer(post=post, owner=request.user.profile, data=comment_data)

    if not serializer.is_valid():
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_new_comments_for_post(request):
    post_id = request.data.get('postId')
    time = request.data.get('time')
    if not post_id:
        return Response({'details': {'required_fields': ['postId']}}, status=status.HTTP_400_BAD_REQUEST)
    if not time:
        return Response({'details': {'required_fields': ['time']}}, status=status.HTTP_400_BAD_REQUEST)

    post_comments = PostComment.objects.filter(post=post_id, created_at__gt=time)
    count = PostComment.objects.filter(post=post_id).count()
    time = datetime.now()
    # paginator = LimitOffsetPaginationTime()
    # paginator.default_limit = 1
    # result_page = paginator.paginate_queryset(post_comments, request)
    # return paginator.get_paginated_response(serializer.data, time)

    serializer = PostCommentSerializer(post_comments, many=True)
    return Response({'results': serializer.data, 'count': count, 'time': time})


@api_view(['POST'])
@permission_classes([AllowAny])
def get_new_comments_for_post_count(request):
    post_id = request.data.get('postId')
    time = request.data.get('time')
    if not post_id:
        return Response({'details': {'required_fields': ['postId']}}, status=status.HTTP_400_BAD_REQUEST)
    if not time:
        time = datetime.now()

    if request.user.is_authenticated:
        count = PostComment.objects.exclude(owner=request.user.profile).filter(post=post_id, created_at__gt=time).count()
    else:
        count = PostComment.objects.filter(post=post_id, created_at__gt=time).count()

    return Response({'count': count, 'postId': post_id}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_comments_for_post(request):
    post_id = request.data.get('postId')
    time = request.data.get('time')
    if not post_id:
        return Response({'details': {'required_fields': ['postId']}}, status=status.HTTP_400_BAD_REQUEST)
    if not time:
        time = datetime.now()

    post_comments = PostComment.objects.filter(post=post_id, created_at__lte=time)

    paginator = LimitOffsetPaginationTime()
    paginator.default_limit = 30
    result_page = paginator.paginate_queryset(post_comments, request)

    serializer = PostCommentSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data, time)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def comment_on_post(request):
#     serializer_context = {'account': request.user}
#     serializer = CommentSerializer(data=request.data, context=serializer_context)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def comment_on_comment(request):
#     comment_id = request.data.get('comment')
#     if not comment_id:
#         return Response({'required': 'comment'})
#
#     try:
#         comment = Comment.objects.get(pk=comment_id)
#     except Comment.DoesNotExist:
#         raise Http404
#
#     if comment.parent is not None:
#         return Response({'error': 'Cannot comment on a comment reply.'}, status=status.HTTP_400_BAD_REQUEST)
#
#     request.data['post'] = comment.post.id
#     request.data['parent'] = comment.id
#     serializer_context = {'account': request.user}
#     serializer = CommentSerializer(data=request.data, context=serializer_context)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_comment(request):
#     comment_id = request.data.get('comment')
#     if not comment_id:
#         return Response({'required': 'post'})
#
#     try:
#         comment = Comment.active.get(pk=comment_id)
#     except Comment.DoesNotExist:
#         raise Http404
#
#     if comment.account != request.user:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#
#     comment.set_deleted()
#     return Response({'deleted': f'{comment}'}, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_comments_on_post(request, post_id):
#     comments = Comment.active.filter(post=post_id, parent=None)
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_comments_on_comment(request, comment_id):
#     comments = Comment.active.filter(parent=comment_id)
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_comment(request, comment_id):
#     try:
#         comment = Comment.objects.get(id=comment_id)
#     except Comment.DoesNotExist:
#         raise Http404
#
#     if comment.account != request.user:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     serializer = CommentSerializer(comment, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
