from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    handle = serializers.CharField(source='account.handle', read_only=True)
    profile_image = serializers.URLField(source='account.profile.image', read_only=True)
    is_private = serializers.BooleanField(source='account.profile.is_private', read_only=True)
    created_at = serializers.SerializerMethodField(method_name='get_created_at', read_only=True)
    updated_at = serializers.SerializerMethodField(method_name='get_updated_at', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'handle', 'profile_image', 'image', 'caption', 'created_at', 'updated_at', 'is_private')
        """
        Meta.read_only_fields does not affects declared fields #3533
        https://github.com/encode/django-rest-framework/issues/3533
        """
        # read_only_fields = ('handle', 'profile_image', 'is_private', 'created_at', 'updated_at')
        # TODO: Read up on optional fields and how they relate to read_only.
        # optional_fields = ('account', 'handle', 'profile_image', 'is_private', 'created_at', 'updated_at')

    def create(self, validated_data):
        account = self.context.get('account')
        return Post.objects.create(account=account, **validated_data)

    """
    For more info on SerializedMethodField and get_<field_name>(self, obj)
    https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    """
    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
