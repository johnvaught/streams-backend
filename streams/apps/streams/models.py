import uuid
from django.db import models
from streams.apps.follows.models import StreamFollow, ProfileFollow
from streams.settings import AUTH_USER_MODEL
from streams.apps.core.models import TimestampedModel


class StreamManager(models.Manager):
    def get_queryset(self):
        return super(StreamManager, self).get_queryset() \
            .select_related('owner').filter(owner__account__is_active=True, is_deleted=False)


class Stream(TimestampedModel):
    """
    For more info on ManyToManyField(through=),
    https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ManyToManyField.through
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    is_private = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    followed_profiles = models.ManyToManyField('profiles.Profile', through='follows.ProfileFollow',
                                               related_name='following_streams')

    objects = StreamManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.is_deleted:
            # also set deleted all the profile follows and stream follows
            profile_follows = ProfileFollow.objects.filter(stream=self.id)
            for profile_follow in profile_follows:
                profile_follow.set_deleted()

            stream_follows = StreamFollow.objects.filter(stream=self.id)
            for stream_follow in stream_follows:
                stream_follow.set_deleted()

        super(Stream, self).save(*args, **kwargs)

    def set_deleted(self):
        self.is_deleted = True
        self.save()
