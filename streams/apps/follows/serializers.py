from rest_framework import serializers
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    profile = serializers.CharField(source='account.profile', read_only=True)

    class Meta:
        model = Follow
        fields = ['profile', 'stream', 'stream_follows_account']
        read_only_fields = ['stream']

    def create(self, validated_data):
        account = self.context.get('account')
        stream = self.context.get('stream')
        return Follow.objects.create(account=account, stream=stream, **validated_data)
