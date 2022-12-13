from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
from .models import User,Following,Comment,Like,Post
from .serializer import FollowSerializer,UserSerializer
class login(APIView):
    def post(self,request):
        try:
            data=request.data
            username=data['username']
            password=data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                return Response({'status':400,'message':"Incorrect credentials"})
            refresh=RefreshToken.for_user(user)
            return Response({'refresh': str(refresh),'access': str(refresh.access_token),'message':"correct credentials"})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class follow(APIView):
    
    permission_classes = (IsAuthenticated,)
    def post(self,request,id):
        try:
            usertofollow = User.objects.get(username=id)
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return Response({'status':404,'message':f"{id} doesnt exist"})
        else:
            try:
                oldfollowobject= Following.objects.get(user=user, userfollowed=usertofollow)
                return Response({'status':400,'message':"You already follow the person"})
            except Following.DoesNotExist:
                newfollowobject = Following(user=request.user, userfollowed=usertofollow)
                newfollowobject.save()
                return Response({'status':200,'message':f"You now follow {usertofollow.username}"})
        

class unfollow(APIView):
    
    permission_classes = (IsAuthenticated,)
    def post(self,request,id):
        try:
            usertounfollow = User.objects.get(username=id)
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return Response({'status':404,'message':f"{id} doesnt exist"})
        else:
            try:
                oldfollowobject= Following.objects.get(user=user, userfollowed=usertounfollow)
                oldfollowobject.delete()
                
                return Response({'status':200,'message':f"You have unfollowed {usertounfollow.username}"})
                
            except Following.DoesNotExist:
                return Response({'status':400,'message':"You already not follwing the person"})
               

class userprofile(APIView):
    
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        userdata = User.objects.get(username=request.user.username)
    # Get following and followed user objects
        following_id_list = Following.objects.filter(user=userdata).values_list('userfollowed', flat=True)
        followers_id_list = Following.objects.filter(userfollowed=userdata).values_list('user', flat=True)
        following_user_list = User.objects.filter(id__in=following_id_list).values('username')
        followers_user_list = User.objects.filter(id__in=followers_id_list).values('username')
        serializerfollowers_user_list=UserSerializer(followers_user_list,many=True)
        serializerfollowing_user_list=UserSerializer(following_user_list,many=True)
        return Response({'status':200,'User Name':userdata.username,'followers':serializerfollowers_user_list.data,'following':serializerfollowing_user_list.data})
        

  