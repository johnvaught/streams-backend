from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import StreamSerializer
from .models import Stream


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_stream(request):
    serializer_context = {'account': request.user}
    serializer = StreamSerializer(data=request.data, context=serializer_context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_stream(request, stream_id):
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404

    if stream.owner != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = StreamSerializer(stream)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def read_public_stream(request, stream_id):
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404

    if stream.is_private:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = StreamSerializer(stream)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_streams(request):
    try:
        streams = Stream.objects.filter(owner=request.user)
    except Stream.DoesNotExist:
        raise Http404

    serializer = StreamSerializer(streams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def read_public_streams_for(request, handle):
    try:
        streams = Stream.objects.filter(owner__handle=handle, is_private=False)
    except Stream.DoesNotExist:
        raise Http404

    serializer = StreamSerializer(streams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_stream(request, stream_id):
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404

    if stream.owner != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = StreamSerializer(stream, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stream(request, stream_id):
    try:
        stream = Stream.objects.get(pk=stream_id)
    except Stream.DoesNotExist:
        raise Http404

    if stream.owner != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    stream.delete()
    return Response({'Deleted': f'{stream}'}, status=status.HTTP_204_NO_CONTENT)
