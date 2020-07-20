from django.http import Http404
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response
from rest_framework import status
from .serializers import ProfileSerializer
from .models import Profile
from streams.apps.posts.models import Post
from streams.apps.follows.models import Follow


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    serializer = ProfileSerializer(request.user.profile)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_profile(request):
    try:
        profileId = request.data['id']
    except KeyError:
        return Response({'details': {'required fields': ['id']}}, status=status.HTTP_400_BAD_REQUEST)

    try:
        profile = Profile.objects.get(pk=profileId)
    except Profile.DoesNotExist:
        raise Http404()

    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def search_profiles(request):
    try:
        query = request.data['query']
    except KeyError:
        return Response({'details': {'required fields': ['query']}}, status=status.HTTP_400_BAD_REQUEST)

    profiles = Profile.objects.filter(Q(account__handle__icontains=query) | Q(full_name__icontains=query))
    serializer = ProfileSerializer(profiles, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_profile(request):
#     serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def read_public_profile(request, handle):
#     try:
#         profile = Profile.objects.select_related('account').get(account__handle=handle)
#     except Profile.DoesNotExist:
#         raise Http404()
#
#     if profile.is_private:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     serializer = ProfileSerializer(profile)
#     return Response(serializer.data, status=status.HTTP_200_OK)

