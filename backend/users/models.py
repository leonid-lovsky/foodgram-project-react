from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db.models import EmailField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    email = EmailField(
        _('email address'),
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
