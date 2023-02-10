from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscribing',
    )
    subscribing = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscribers',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscribing'],
                name='unique subscription'
            ),
        ]

    def clean(self):
        if self.subscriber == self.subscribing:
            raise ValidationError(_('You can\'t subscribe to yourself!'))
