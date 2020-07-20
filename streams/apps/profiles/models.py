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
    bio = models.TextField(max_length=1000, blank=True, default="")
    last_stream = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)

    objects = ProfileManager()

    def add_follower(self):
        # take in follower id
        # check if duplicate
        pass

    def __str__(self):
        return self.account.handle


# class ProfileFollows(TimestampedModel):
#     account = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

