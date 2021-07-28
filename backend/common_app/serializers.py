from django.contrib.auth.models import User, Group
from common_app.utils import BaseModelSerializer


class GroupSerializer(BaseModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(BaseModelSerializer):
    # groups = GroupSerializer()

    class Meta:
        model = User
        fields = ['username', 'email']
