from rest_framework import serializers
from .models import Stream


class StreamSerializer(serializers.ModelSerializer):
    handle = serializers.CharField(source='owner.handle', read_only=True)

    class Meta:
        model = Stream
        fields = ('id', 'handle', 'name', 'is_private')
        extra_kwargs = {
            'is_private': {'write_only': True},
        }

    def create(self, validated_data):
        account = self.context.get('account')
        return Stream.objects.create(owner=account, **validated_data)
