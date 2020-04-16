from django.db import models
from streams.apps.core.models import TimestampedModel


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().select_related('account')\
            .filter(account__is_active=True, is_deleted=False)


class Post(TimestampedModel):
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, related_name='posts')
    image = models.URLField(blank=True, default='')
    caption = models.CharField(max_length=2200, blank=True, default='')
    is_deleted = models.BooleanField(default=False)

    objects = PostManager()

    def __str__(self):
        return f'{self.account.handle} : {self.caption[:20]}'

    def delete(self):
        self.is_deleted = True
        self.save()
