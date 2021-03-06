import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeHandleValidator
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from streams.apps.core.models import TimestampedModel


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, handle, email, password, **extra_fields):
        """
        Create and save an account with the given handle, email, and password.
        """
        if not handle:
            raise ValueError('The given handle must be set')
        email = self.normalize_email(email)
        handle = self.model.normalize_username(handle)
        user = self.model(handle=handle, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # When a user is created, an associated one-to-one profile
        # must be created as well.
        # Profile.objects.create(account=user)
        # ^ I do this in the serializer now
        # which means if i create an account not with my webapp there is no profile associated.

        return user

    def create_user(self, handle, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(handle, email, password, **extra_fields)

    def create_superuser(self, handle, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(handle, email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    handle_validator = UnicodeHandleValidator()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    handle = models.CharField(
        _('handle'),
        max_length=15,
        unique=True,
        help_text=_('Required. 15 characters or fewer. Letters, digits and ./+/-/_ only.'),
        db_index=True,
        validators=[handle_validator],
        error_messages={
            'unique': _("A user with that handle already exists."),
        }, )
    email = models.EmailField(_('email address'), max_length=128, blank=True)
    phone = models.CharField(_('phone number'), max_length=28, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = AccountManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'handle'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """Return the full name for the user."""
        return self.handle

    def get_short_name(self):
        """Return the short name for the user."""
        return self.handle

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def set_inactive(self):
        self.is_active = False
        self.save()


