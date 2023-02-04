from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'password'
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
