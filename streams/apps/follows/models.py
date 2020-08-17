import uuid
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models import Q
# from streams.settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError

from streams.apps.core.models import TimestampedModel
from django.utils.translation import gettext_lazy as _


class FollowManager(models.Manager):
    def get_queryset(self):
        """
        Only query when accounts and streams that have not been `deleted`.
        """
        return super(FollowManager, self).get_queryset()\
            .select_related('profile', 'stream')\
            .filter(profile__account__is_active=True, stream__owner__account__is_active=True,
                    stream__is_deleted=False, is_deleted=False)


class StreamFollow(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    stream = models.ForeignKey('streams.Stream', on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=False)

    objects = FollowManager()

    class Meta:
        """
        A profile cannot follow a stream multiple times.
        """
        constraints = [
            UniqueConstraint(fields=['stream', 'profile'], condition=Q(is_deleted=False),
                             name='unique_stream_follow')
        ]

    def __str__(self):
        return f'{self.profile} follows {self.stream} '

    def set_deleted(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):
        if self.profile == self.stream.owner:
            # TODO: Remove testing print
            print('TESTING: Validation error called from Follows.save')
            raise Exception(_('You may not follow your own stream.'))

        if self.is_deleted:
            self.stream.owner.cond_remove_from_follower_count_for_stream_follow(self)
            self.profile.cond_remove_from_following_count_for_stream_follow(self)

        if not self.is_deleted:
            self.stream.owner.cond_add_to_follower_count_for_stream_follow(self)
            self.profile.cond_add_to_following_count_for_stream_follow(self)

        super(StreamFollow, self).save(*args, **kwargs)


class ProfileFollow(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stream = models.ForeignKey('streams.Stream', on_delete=models.CASCADE)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=False)

    objects = FollowManager()

    class Meta:
        """
        A stream cannot follow a profile multiple times.
        """
        constraints = [
            UniqueConstraint(fields=['stream', 'profile'], condition=Q(is_deleted=False),
                             name='unique_profile_follow')
        ]

    def __str__(self):
        return f'{self.stream} follows {self.profile} '

    def set_deleted(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):
        if self.profile == self.stream.owner:
            # TODO: Remove testing print
            print('TESTING: Validation error called from Follows.save')
            raise Exception(_('You may not follow your own account.'))

        if self.is_deleted:
            self.stream.owner.cond_remove_from_following_count(self.profile, self.stream)
            self.profile.cond_remove_from_follower_count(self.stream.owner, self.stream)

        if not self.is_deleted:
            self.stream.owner.cond_add_to_following_count(self.profile, self.stream)
            self.profile.cond_add_to_follower_count(self.stream.owner, self.stream)
            # pass

        super(ProfileFollow, self).save(*args, **kwargs)


# class Follow(TimestampedModel):
#     followee = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='followee')
#     follower = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='follower')
#     streams = models.ManyToManyField('streams.Stream', related_name='follows', blank=True)
#
#     @property
#     def is_active(self):
#         return False
#
#     objects = FollowManager()
#
#     class Meta:
#         unique_together = ('followee', 'follower')
#
#     def __str__(self):
#         return f'{self.follower.handle} follows {self.followee.handle} '
#

# class Follow(TimestampedModel):
#     """
#     If stream_follows_account is true, then the stream is following an account.
#     If false, an account is following a public stream.
#     """
#     profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
#     stream = models.ForeignKey('streams.Stream', on_delete=models.CASCADE)
#     stream_follows_account = models.BooleanField()
#     is_deleted = models.BooleanField(default=False)
#
#     objects = FollowManager()
#
#     @property
#     def stream_owner(self):
#         return self.stream.owner
#
#     class Meta:
#         """
#         A stream cannot follow an account multiple times, and vice versa.
#         """
#         unique_together = ('profile', 'stream', 'stream_follows_account')
#
#     def __str__(self):
#         return f'account:{self.profile.handle} :: stream owner:{self.stream.owner}, stream:{self.stream.name}'
#
#     def clean(self):
#         """
#         A stream may not follow their creator to avoid creating false followers.
#         An account may not follow their own stream to prevent duplicate follows,
#         since the stream creator already inherits the account followed.
#
#         For more info on clean()
#         https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model.clean
#         https://stackoverflow.com/questions/4441539/why-doesnt-djangos-model-save-call-full-clean
#         # TODO: Is clean called from Serializer.is_validated?
#         """
#         if self.stream.owner == self.profile:
#             # TODO: Remove testing print
#             print('TESTING: Validation error called from Follows.clean')
#             raise ValidationError({'error': _('You may not follow your own account or stream.')})
#
#     def set_deleted(self):
#         self.is_deleted = True
#         self.save()
#
#     def save(self, *args, **kwargs):
#         if self.profile == self.stream.owner:
#             # TODO: Remove testing print
#             print('TESTING: Validation error called from Follows.save')
#             raise Exception(_('You may not follow your own account or stream.'))
#         super(Follow, self).save(*args, **kwargs)
