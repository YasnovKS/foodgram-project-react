from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Subscribe

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        author = obj
        follower = self.context.get('request').user

        return Subscribe.objects.filter(follower=follower,
                                        author=author).exists()
