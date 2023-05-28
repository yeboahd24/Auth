from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.core.validators import EmailValidator


class CustomUser(AbstractBaseUser):
    """A custom user model that allows sign up with email or phone"""

    email_or_phone = models.CharField(
        _("Email or Phone"),
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$|^([\w.%+-]+)@([\w-]+\.)+([\w]{2,})$",
                message=_("Please enter a valid email address or phone number.")
            ),
        ],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email_or_phone"
    EMAIL_FIELD = "email_or_phone"

    def __str__(self):
        return self.email_or_phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.is_staff
