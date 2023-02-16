from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db.models import (
    CASCADE, EmailField, ForeignKey, Model, UniqueConstraint
)
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    email = EmailField(
        _('email address'),
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Subscription(Model):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='following',
    )
    author = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='followers',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def clean(self):
        if self.user == self.author:
            raise ValidationError(_('You can\'t subscribe to yourself!'))
