from rest_framework import serializers
from .models import User,Following,Post,Comment


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model=Following
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['username']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ['title','content']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields = ['content']

class AllPostSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True)
    likes = serializers.StringRelatedField(many=True)
    class Meta:
        model=Post
        fields =['id','title','content','date','comments','likes']