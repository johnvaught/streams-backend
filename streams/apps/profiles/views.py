from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response
from rest_framework import status
from .serializers import ProfileSerializer
from .models import Profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_profile(request):
    profile = ProfileSerializer(request.user)
    return Response(profile.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = ProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    print(serializer.validated_data)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def read_public_profile(request, handle):
    try:
        profile = Profile.objects.select_related('account').get(account__handle=handle)
    except Profile.DoesNotExist:
        raise Http404()

    if profile.is_private:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)
