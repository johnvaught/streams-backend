from rest_framework import serializers
from .models import Profile
from streams.settings import DEFAULT_PROFILE_IMAGE


class ProfileSerializer(serializers.ModelSerializer):
    handle = serializers.CharField(source='account.handle', read_only=True)
    phone = serializers.CharField(source='account.phone', read_only=True)
    email = serializers.CharField(source='account.email', read_only=True)
    post_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'handle', 'phone', 'email', 'full_name', 'bio', 'image', 'is_private', 'post_count',
                  'follower_count', 'following_count']
        optional_fields = ['bio', 'full_name', 'image', 'is_private']
        # read_only_fields = ('handle', 'phone', 'email')
        extra_kwargs = {
            'is_private': {'write_only': True},
        }

    """
    For more info on SerializedMethodField and get_<field_name>(self, obj)
    https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    """
    def get_image(self, obj):
        if obj.image:
            return obj.image

        return DEFAULT_PROFILE_IMAGE

    def get_post_count(self, obj):
        return obj.account.posts.count()
