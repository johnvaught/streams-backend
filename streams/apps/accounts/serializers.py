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
        token['handle'] = user.handle

        return token


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['handle'] = user.handle

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

        for (key, value) in profile_data.items():
            setattr(profile, key, value)
        profile.save()

        return instance
