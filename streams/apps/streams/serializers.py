from rest_framework import serializers
from .models import Stream


class StreamSerializer(serializers.ModelSerializer):
    handle = serializers.CharField(source='owner.handle', read_only=True)

    class Meta:
        model = Stream
        fields = ('id', 'owner', 'handle', 'name', 'is_private')
        extra_kwargs = {
            'is_private': {'write_only': True},
        }

    def create(self, validated_data):
        profile = self.context.get('profile')
        return Stream.objects.create(owner=profile, **validated_data)
