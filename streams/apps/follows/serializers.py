from rest_framework import serializers
from .models import StreamFollow, ProfileFollow


class StreamFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamFollow
        fields = ['profile', 'stream', 'is_deleted']
        read_only_fields = ['profile', 'stream']

    def create(self, validated_data):
        profile = self.context.get('profile')
        stream = self.context.get('stream')
        return StreamFollow.objects.create(profile=profile, stream=stream, **validated_data)


class ProfileFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileFollow
        fields = ['profile', 'stream', 'is_deleted']
        read_only_fields = ['profile', 'stream']

    def create(self, validated_data):
        profile = self.context.get('profile')
        stream = self.context.get('stream')
        return ProfileFollow.objects.create(profile=profile, stream=stream, **validated_data)
