from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField(method_name='get_created_at', read_only=True)
    updated_at = serializers.SerializerMethodField(method_name='get_updated_at', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'parent', 'account', 'caption', 'is_deleted', 'created_at', 'updated_at']
        read_only_fields = ['account', 'is_deleted']

    def create(self, validated_data):
        account = self.context.get('account')
        # post = self.context.get('post')
        return Comment.objects.create(account=account, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
