from django.db import models
from streams.apps.core.models import TimestampedModel
from streams.settings import AUTH_USER_MODEL


class ProfileManager(models.Manager):
    """
    Inactivating an account also `deletes` the associated profile by
    removing them from all queries.
    """
    # TODO: Research .select_related() because I'm pretty sure I could be using it better.
    def get_queryset(self):
        return super(ProfileManager, self).get_queryset()\
            .select_related('account').filter(account__is_active=True)


class Profile(TimestampedModel):
    account = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    image = models.URLField(blank=True, default="")
    bio = models.TextField(max_length=150, blank=True, default="")
    is_private = models.BooleanField(default=False)

    objects = ProfileManager()

    def __str__(self):
        return self.account.handle
