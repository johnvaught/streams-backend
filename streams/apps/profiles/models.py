from django.db import models
from streams.apps.core.models import TimestampedModel
from streams.settings import AUTH_USER_MODEL


class ProfileManager(models.Manager):
    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().select_related('account').filter(account__is_active=True)


class PublicProfileManager(models.Manager):
    def get_queryset(self):
        return super(PublicProfileManager, self).get_queryset().filter(is_private=False)


class Profile(TimestampedModel):
    account = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    image = models.URLField(blank=True, default="")
    bio = models.TextField(max_length=150, blank=True, default="")
    is_private = models.BooleanField(default=False)

    objects = ProfileManager()
    public_profiles = PublicProfileManager()

    def __str__(self):
        return self.account.handle
