import uuid
from django.db import models
from streams.apps.core.models import TimestampedModel


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().select_related('owner')\
            .filter(owner__account__is_active=True, is_deleted=False)


class Post(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='posts')
    image = models.CharField(max_length=36, blank=True, default='')
    caption = models.CharField(max_length=2200, blank=True, default='')
    is_deleted = models.BooleanField(default=False)

    objects = PostManager()

    def __str__(self):
        return f'{self.owner.handle} : {self.caption[:20]}'

    def set_deleted(self):
        self.is_deleted = True
        self.save()
