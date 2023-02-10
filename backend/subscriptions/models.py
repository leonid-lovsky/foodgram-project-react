from django.conf import settings
from django.db.models import CASCADE, ForeignKey, Model, UniqueConstraint
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class Subscription(Model):
    subscriber = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='subscribing',
    )
    subscribing = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='subscribers',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['subscriber', 'subscribing'],
                name='unique subscription'
            ),
        ]

    def clean(self):
        if self.subscriber == self.subscribing:
            raise ValidationError(_('You can\'t subscribe to yourself!'))
