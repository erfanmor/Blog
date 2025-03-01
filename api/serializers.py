from rest_framework.serializers import ModelSerializer
from account.models import CustomUser
from post.models import Post


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class ListUsersSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'age', 'email', 'number']


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'date', 'view_count', 'photo', 'tags']


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'age',
                  'number', 'address', 'photo', 'date_joined']
