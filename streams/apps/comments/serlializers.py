from rest_framework import serializers
from .models import PostComment

from streams.settings import DEFAULT_PROFILE_IMAGE


class PostCommentSerializer(serializers.ModelSerializer):
    handle = serializers.CharField(source='owner.handle', read_only=True)
    profile_image = serializers.SerializerMethodField(read_only=True)
    # created_at = serializers.SerializerMethodField(method_name='get_created_at', read_only=True)
    # updated_at = serializers.SerializerMethodField(method_name='get_updated_at', read_only=True)

    class Meta:
        model = PostComment
        fields = ['id', 'post', 'owner', 'handle', 'profile_image', 'text', 'is_deleted', 'created_at', 'updated_at']
        read_only_fields = ('id', 'post', 'owner')

    def create(self, validated_data):
        id = self.context.get('id')
        post = self.context.get('post')
        owner = self.context.get('owner')
        return PostComment.objects.create(id=id, post=post, owner=owner, **validated_data)

    @staticmethod
    def get_profile_image(instance):
        if instance.owner.image:
            return instance.owner.image
        return DEFAULT_PROFILE_IMAGE

    @staticmethod
    def get_created_at(instance):
        return instance.created_at.isoformat()

    @staticmethod
    def get_updated_at(instance):
        return instance.updated_at.isoformat()

# class CommentSerializer(serializers.ModelSerializer):
#     created_at = serializers.SerializerMethodField(method_name='get_created_at', read_only=True)
#     updated_at = serializers.SerializerMethodField(method_name='get_updated_at', read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'parent', 'account', 'caption', 'is_deleted', 'created_at', 'updated_at']
#         read_only_fields = ['account', 'is_deleted']
#
#     def create(self, validated_data):
#         account = self.context.get('account')
#         # post = self.context.get('post')
#         return Comment.objects.create(account=account, **validated_data)
#
#     def get_created_at(self, instance):
#         return instance.created_at.isoformat()
#
#     def get_updated_at(self, instance):
#         return instance.updated_at.isoformat()
