from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False)
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
