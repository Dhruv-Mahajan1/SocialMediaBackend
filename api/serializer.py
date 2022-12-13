from rest_framework import serializers
from .models import User,Following


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model=Following
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['username']