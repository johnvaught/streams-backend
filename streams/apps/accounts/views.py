from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response
from rest_framework import status
from .serializers import AccountSerializer, MyTokenObtainPairSerializer, MyTokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from streams.apps.profiles.serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_account(request):
    print(request.data)
    account_serializer = AccountSerializer(data=request.data)
    account_serializer.is_valid(raise_exception=True)
    account = account_serializer.save()

    # profile_serializer = ProfileSerializer(data=request.data.profile)
    # profile_serializer.is_valid(raise_exception=True)
    # profile_serializer.save()

    refresh = RefreshToken.for_user(account)
    response = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'authProfileId': str(refresh.authProfileId),
    }
    return Response(response, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_account(request):
#     print(request.data)
#     # account_serializer = AccountSerializer(data=request.data)
#     # account_serializer.is_valid(raise_exception=True)
#     # account = account_serializer.save()
#     #
#     # # profile_serializer = ProfileSerializer(data=request.data.profile)
#     # # profile_serializer.is_valid(raise_exception=True)
#     # # profile_serializer.save()
#     #
#     # refresh = RefreshToken.for_user(account)
#     # tokens = {
#     #     'refresh': str(refresh),
#     #     'access': str(refresh.access_token),
#     # }
#     return Response('created!', status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def read_account(request):
#     account = AccountSerializer(request.user)
#     return Response(account.data)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def update_account(request):
#     serializer = AccountSerializer(request.user, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     print(serializer.validated_data)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_account(request):
#     request.user.set_inactive()
#     return Response({'Deleted': f'{request.user}'}, status=status.HTTP_204_NO_CONTENT)
