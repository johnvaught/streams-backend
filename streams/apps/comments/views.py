from django.http import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from streams.apps.posts.models import Post
from .serlializers import CommentSerializer
from .models import Comment


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_post(request):
    serializer_context = {'account': request.user}
    serializer = CommentSerializer(data=request.data, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_on_comment(request):
    comment_id = request.data.get('comment')
    if not comment_id:
        return Response({'required': 'comment'})

    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise Http404

    if comment.parent is not None:
        return Response({'error': 'Cannot comment on a comment reply.'}, status=status.HTTP_400_BAD_REQUEST)

    request.data['post'] = comment.post.id
    request.data['parent'] = comment.id
    serializer_context = {'account': request.user}
    serializer = CommentSerializer(data=request.data, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request):
    comment_id = request.data.get('comment')
    if not comment_id:
        return Response({'required': 'post'})

    try:
        comment = Comment.active.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise Http404

    if comment.account != request.user:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    comment.set_deleted()
    return Response({'deleted': f'{comment}'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_comments_on_post(request, post_id):
    comments = Comment.active.filter(post=post_id, parent=None)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_comments_on_comment(request, comment_id):
    comments = Comment.active.filter(parent=comment_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise Http404

    if comment.account != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = CommentSerializer(comment, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
