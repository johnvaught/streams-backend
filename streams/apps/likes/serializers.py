from rest_framework import serializers
from .models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    handle = serializers.CharField(source='owner.handle', read_only=True)
    # created_at = serializers.SerializerMethodField(method_name='get_created_at', read_only=True)
    # updated_at = serializers.SerializerMethodField(method_name='get_updated_at', read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'handle', 'post']
        # read_only_fields = ['owner']

    def create(self, validated_data):
        post = self.context.get('post')
        owner = self.context.get('owner')
        return PostLike.objects.create(post=post, owner=owner, **validated_data)

    # @staticmethod
    # def get_created_at(instance):
    #     return instance.created_at.isoformat()
    #
    # @staticmethod
    # def get_updated_at(instance):
    #     return instance.updated_at.isoformat()


# class LikeSerializer(serializers.ModelSerializer):
#     created_at = serializers.SerializerMethodField(method_name='get_created_at', read_only=True)
#     updated_at = serializers.SerializerMethodField(method_name='get_updated_at', read_only=True)
#
#     class Meta:
#         model = Like
#         fields = ['id', 'account', 'post', 'comment', 'created_at', 'updated_at']
#         read_only_fields = ['account', 'is_deleted']
#
#     def create(self, validated_data):
#         account = self.context.get('account')
#         return Like.objects.create(account=account, **validated_data)
#
#     def get_created_at(self, instance):
#         return instance.created_at.isoformat()
#
#     def get_updated_at(self, instance):
#         return instance.updated_at.isoformat()
