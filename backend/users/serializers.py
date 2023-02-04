from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (HyperlinkedIdentityField,
                                        SerializerMethodField)

# from .models import Subscription

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'password'
        ]
        extra_kwargs = {
            'email': {
                'required': True, 'allow_blank': False
            },
            'username': {
                'required': True, 'allow_blank': False
            },
            'first_name': {
                'required': True, 'allow_blank': False
            },
            'last_name': {
                'required': True, 'allow_blank': False
            },
            'password': {
                'required': True, 'allow_blank': False
            },
        }


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        return False  # TODO
        # user = self.context.get('request').user
        # if user.is_anonymous:
        # return False
        # return Subscription.objects.filter(user=user, author=obj).exists()
