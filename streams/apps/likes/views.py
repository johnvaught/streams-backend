from django.http import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from streams.apps.posts.models import Post
from .serializers import LikeSerializer
from .models import Like
from streams.apps.comments.models import Comment


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like_comment(request, comment_id):
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
