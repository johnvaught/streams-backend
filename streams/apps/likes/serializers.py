from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField(method_name='get_created_at', read_only=True)
    updated_at = serializers.SerializerMethodField(method_name='get_updated_at', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'account', 'post', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['account', 'is_deleted']

    def create(self, validated_data):
        account = self.context.get('account')
        return Like.objects.create(account=account, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
