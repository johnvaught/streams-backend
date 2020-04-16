from django.db import models
from streams.settings import AUTH_USER_MODEL
from streams.apps.core.models import TimestampedModel
from streams.apps.accounts.models import Account


class StreamManager(models.Manager):
    def get_queryset(self):
        return super(StreamManager, self).get_queryset().select_related('owner')\
            .filter(owner__is_active=True, is_deleted=False)


class Stream(TimestampedModel):
    """
    For more info on ManyToManyField(through=),
    https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ManyToManyField.through
    """
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # account = models.ManyToManyField(AUTH_USER_MODEL, through='follows.Follow',
    #                                  symmetrical=False, related_name='streams')
    name = models.CharField(max_length=15)
    is_private = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = StreamManager()

    def __str__(self):
        return self.name
