from django.conf import settings
from django.db.models import CASCADE, ForeignKey, Model, UniqueConstraint
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class Subscription(Model):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        # related_name='authors',
    )
    author = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        # related_name='users',
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
