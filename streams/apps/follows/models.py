from django.db import models
from streams.settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from streams.apps.core.models import TimestampedModel
from django.utils.translation import gettext_lazy as _


class FollowManager(models.Manager):
    def get_queryset(self):
        """
        Only query accounts and streams that have not been `deleted`.
        """
        # TODO: There's no way I'm using select_related correctly.
        return super(FollowManager, self).get_queryset()\
            .select_related('account').filter(account__is_active=True)\
            .select_related('stream').filter(stream__is_deleted=False)


class Follow(TimestampedModel):
    """
    If stream_follows_account is true, then the stream is following an account.
    If false, an account is following a public stream.
    """
    account = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    stream = models.ForeignKey('streams.Stream', on_delete=models.CASCADE)
    stream_follows_account = models.BooleanField()
    is_deleted = models.BooleanField(default=False)

    objects = FollowManager()

    class Meta:
        """
        A stream cannot follow an account multiple times, and vice versa.
        """
        unique_together = ('account', 'stream', 'stream_follows_account')

    def __str__(self):
        return f'account:{self.account.handle} :: stream owner:{self.stream.owner}, stream:{self.stream.name}'

    def clean(self):
        """
        A stream may not follow their creator to avoid creating false followers.
        An account may not follow their own stream to prevent duplicate follows,
        since the stream creator already inherits the account followed.

        For more info on clean()
        https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model.clean
        https://stackoverflow.com/questions/4441539/why-doesnt-djangos-model-save-call-full-clean
        # TODO: Is clean called from Serializer.is_validated?
        """
        if self.stream.account == self.account:
            # TODO: Remove testing print
            print('TESTING: Validation error called from Follows.clean')
            raise ValidationError({'error': _('You may not follow your own account or stream.')})

    def set_deleted(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):
        if self.account == self.stream.owner:
            # TODO: Remove testing print
            print('TESTING: Validation error called from Follows.save')
            raise Exception(_('You may not follow your own account or stream.'))
        super(Follow, self).save(*args, **kwargs)
