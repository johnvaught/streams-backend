from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response
from rest_framework import status
from .serializers import AccountSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_account(request):
    serializer = AccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_account(request):
    account = AccountSerializer(request.user)
    return Response(account.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_account(request):
    serializer = AccountSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    print(serializer.validated_data)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    request.user.set_inactive()
    return Response({'Account deleted.'}, status=status.HTTP_204_NO_CONTENT)
