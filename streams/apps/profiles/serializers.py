from rest_framework import serializers
from .models import Profile
from streams.settings import DEFAULT_PROFILE_IMAGE


class ProfileSerializer(serializers.ModelSerializer):
    handle = serializers.CharField(source='account.handle', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['handle', 'bio', 'image', 'is_private']
        optional_fields = ['bio', 'image', 'is_private']
        # read_only_fields = ('handle',)
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
