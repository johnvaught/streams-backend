from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import Account
from streams.apps.profiles.serializers import ProfileSerializer
from streams.apps.profiles.models import Profile
from streams.settings import DEFAULT_PROFILE_IMAGE


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['authProfileId'] = user.profile.id

        return token


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['authProfileId'] = user.profile.id

        return token


class AccountSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Account
        fields = ['id', 'handle', 'email', 'phone', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        account = Account.objects.create_user(**validated_data)
        Profile.objects.create(account=account, **profile_data)
        return account

    def update(self, instance, validated_data):
        """Performs an update on an account."""
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        profile.full_name = profile_data.get('full_name', profile.full_name)
        profile.image = profile_data.get('image', profile.image)
        profile.bio = profile_data.get('bio', profile.bio)

        profile.save()

        return instance
