from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(_('date joined'), default=timezone.now)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed.
        ordering = ['-created_at', '-updated_at']
