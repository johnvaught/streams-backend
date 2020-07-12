from django.http import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from streams.apps.posts.models import Post
from .serializers import LikeSerializer
from .models import Like
from streams.apps.comments.models import Comment
from streams.apps.posts.models import Post


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request):
    try:
        comment_id = request.data['comment_id']
    except KeyError:
        return Response({'details': {'required fields': ['comment_id']}}, status=status.HTTP_400_BAD_REQUEST)
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        raise Http404

    request.data['comment'] = comment.id
    serializer_context = {'account': request.user}
    serializer = LikeSerializer(data=request.data, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request):
    try:
        account = request.data['account']
        post = request.data['post']
    except KeyError:
        return Response({'details': {'required fields': ['account', 'post']}}, status=status.HTTP_400_BAD_REQUEST)

    if account != request.user.id:
        return Response({'details': 'you may only like for your account.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        like = Like.objects.get(post=post, account=account)
    except Like.DoesNotExist:
        serializer_context = {'account': request.user}
        serializer = LikeSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        like.is_deleted = False
        like.save()
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request):
    try:
        account = request.data['account']
        likeId = request.data['like']
    except KeyError:
        return Response({'details': {'required fields': ['account', 'like']}}, status=status.HTTP_400_BAD_REQUEST)

    if account != request.user.id:
        return Response({'details': 'you may only unlike for your account.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        like = Like.objects.get(pk=likeId)
    except Like.DoesNotExist:
        raise Http404('Like with that id not found.')

    like.is_deleted = True
    like.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_post_likes_for_account(request):
    try:
        account_id = request.data['account_id']
    except KeyError:
        return Response({'details': {'required fields': ['account_id']}}, status=status.HTTP_400_BAD_REQUEST)
    likes = Like.active.filter(account=account_id, post__isnull=False)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_comment_likes_for_account(request):
    try:
        account_id = request.data['account_id']
    except KeyError:
        return Response({'details': {'required fields': ['account_id']}}, status=status.HTTP_400_BAD_REQUEST)
    likes = Like.objects.filter(account=account_id, comment__isnull=False)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def delete_all_likes(request):
    Like.objects.all().delete()
    return Response('oh boy, i hope you know what you have done', status=status.HTTP_200_OK)