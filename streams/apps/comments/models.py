import uuid
from django.db import models
from streams.apps.core.models import TimestampedModel
from streams.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _


# In the case the account or comment is deleted and it has children, we wan't to
# mark it deleted in the UI, not hide it completely.
class PostCommentManager(models.Manager):
    def get_queryset(self):
        return super(PostCommentManager, self).get_queryset().select_related('owner')\
            .filter(owner__account__is_active=True, post__is_deleted=False, is_deleted=False)


class PostComment(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', related_name='comments', on_delete=models.CASCADE,  db_index=True)
    text = models.CharField(max_length=2200, null=False, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = PostCommentManager()

    def __str__(self):
        return f'profile: {self.owner.handle}, comment: {self.text[:20]}'

    # class Meta:
    #     ordering = ['created_at']

# class Comment(TimestampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
#     post = models.ForeignKey('posts.Post', related_name='comments', on_delete=models.CASCADE)
#     parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, default=None)
#     caption = models.CharField(max_length=2200)
#     is_deleted = models.BooleanField(default=False)
#
#     objects = models.Manager()
#     active = CommentManager()
#
#     def __str__(self):
#         return f'profile: {self.owner.handle}, comment: {self.caption[:20]}'
#
#     def set_deleted(self):
#         self.is_deleted = True
#         self.save()
