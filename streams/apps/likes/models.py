from django.db import models
from streams.apps.core.models import TimestampedModel
from streams.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _


class LikeManager(models.Manager):
    def get_queryset(self):
        return super(LikeManager, self).get_queryset().select_related('owner')\
            .filter(owner__account__is_active=True, is_deleted=False)


class Like(TimestampedModel):
    owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, db_index=True)
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE, null=True, db_index=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    active = LikeManager()

    class Meta:
        models.UniqueConstraint(fields=['account', 'post', 'comment'], name='no_double_likes')
        models.UniqueConstraint(fields=['post', 'comment'], name='comment_XOR_post')

    def __str__(self):
        return f'{self.owner.handle} likes {self.post}{self.comment}'

    def unlike(self):
        self.is_deleted = True
        self.save()

