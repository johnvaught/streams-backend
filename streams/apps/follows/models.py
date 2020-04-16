from django.db import models
from streams.settings import AUTH_USER_MODEL
from django.core.exceptions import ValidationError
from streams.apps.core.models import TimestampedModel
from django.utils.translation import gettext_lazy as _


class FollowManager(models.Manager):
    def get_queryset(self):
        return super(FollowManager, self).get_queryset().filter(followed=True)\
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

    def clean(self):
        """
        A stream may not follow their creator to avoid creating false followers.
        An account may not follow their own stream to prevent duplicate follows,
        since the stream creator already inherits the account followed.

        For more info on clean()
        https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model.clean
        https://stackoverflow.com/questions/4441539/why-doesnt-djangos-model-save-call-full-clean
        # TODO: Calling is_validated() from the serializer does call clean()?
        """
        if self.stream.account == self.account:
            raise ValidationError({'error': _('You may not follow your own account.')})

    def __str__(self):
        return f'{self.account.handle} : {self.stream.name}'
