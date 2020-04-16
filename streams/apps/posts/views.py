from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer_context = {'account': request.user}
    serializer = PostSerializer(data=request.data, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def read_public_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404

    if post.account.profile.is_private:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def read_public_posts_for(request, handle):
    since_date = request.query_params.get('since')
    print(since_date)
    if since_date:
        posts = Post.objects.filter(account__handle=handle, created_at__gt=since_date)
    else:
        posts = Post.objects.filter(account__handle=handle)
    if not posts:
        raise Http404
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404

    if post.account != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = PostSerializer(post, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404

    """
    Object level permissions classes not supported for function based views.
    https://github.com/encode/django-rest-framework/issues/1697
    Workaround below.
    """
    if post.account != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    post.delete()
    return Response({'Deleted': f'{post}'}, status=status.HTTP_204_NO_CONTENT)
