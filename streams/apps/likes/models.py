import uuid
from django.db import models
from streams.apps.core.models import TimestampedModel
from django.db.models.constraints import UniqueConstraint
from django.db.models import Q
from streams.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _


class LikeManager(models.Manager):
    def get_queryset(self):
        return super(LikeManager, self).get_queryset().select_related('owner')\
            .filter(owner__account__is_active=True, post__is_deleted=False, is_deleted=False)


class PostLike(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, db_index=True)
    is_deleted = models.BooleanField(default=False)

    objects = LikeManager()

    class Meta:
        """
        A profile cannot like a post multiple times.
        """
        constraints = [
            UniqueConstraint(fields=['owner', 'post'], condition=Q(is_deleted=False),
                             name='unique_post_like')
        ]

    def __str__(self):
        return f'{self.owner.handle} likes {self.post}'

    def unlike(self):
        self.is_deleted = True
        self.save()


# class Like(TimestampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
#     post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, db_index=True)
#     comment = models.ForeignKey('comments.PostComment', on_delete=models.CASCADE, null=True, db_index=True)
#     is_deleted = models.BooleanField(default=False)
#
#     objects = models.Manager()
#     active = LikeManager()
#
#     class Meta:
#         models.UniqueConstraint(fields=['account', 'post', 'comment'], name='no_double_likes')
#         models.UniqueConstraint(fields=['post', 'comment'], name='comment_XOR_post')
#
#     def __str__(self):
#         return f'{self.owner.handle} likes {self.post}{self.comment}'
#
#     def unlike(self):
#         self.is_deleted = True
#         self.save()
#
