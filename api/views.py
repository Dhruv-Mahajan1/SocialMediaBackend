from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
from .models import User,Following,Comment,Like,Post
from .serializer import FollowSerializer,UserSerializer,PostSerializer,CommentSerializer,AllPostSerializer
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
        

  
class PostAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user =User.objects.get(username=request.user.username)
        post_data = request.data
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            new_post = Post.objects.create(
            postedbyuser=user,
            title=post_data['title'],
            content=post_data['content']
        )
            new_post.save()
            return Response({'Post_id':new_post.id,'title':serializer.data['title'],"content":serializer.data['content'],"Created Time":new_post.date})

        else :
            return Response({'status':404,'message':"Something went wrong"})
        

class DeletePostAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,id):
        user =User.objects.get(username=request.user.username)
        try:
            post =Post.objects.get(id=id)
        except:
            return Response({'Message':"Post doesnt exist"},status=status.HTTP_404_NOT_FOUND)

        if post.postedbyuser != request.user:
            return Response({'Message':"You are not the owner"},status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({'Message':"Post successfully deleted"},status=status.HTTP_204_NO_CONTENT)  



class LikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,id):
        user =User.objects.get(username=request.user.username)
        try:
            post =Post.objects.get(id=id)
        except:
            return Response({'Message':"Post doesnt exist"},status=status.HTTP_404_NOT_FOUND)
        try:
            likeobj =Like.objects.get(post=post,likedbyuser=user)
        except:
            newlikeobj= Like.objects.create(
            likedbyuser=user,
            likes=1,
            post=post
            )
            newlikeobj.save()
            return Response({'Message':f"You liked the post {post.title}"},status=status.HTTP_201_CREATED) 
        else:
            if likeobj.likes>=1:
                return Response({'Message':"You have already liked the post"},status=status.HTTP_403_FORBIDDEN)
            else:
                likeobj.likes=1
                likeobj.dislikes=0
                likeobj.save()

                return Response({'Message':f"You liked the post {post.title}"},status=status.HTTP_201_CREATED)

            

        
class DislikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,id):
        user =User.objects.get(username=request.user.username)
        try:
            post =Post.objects.get(id=id)
        except:
            return Response({'Message':"Post doesnt exist"},status=status.HTTP_404_NOT_FOUND)
        try:
            likeobj =Like.objects.get(post=post,likedbyuser=user)
        except:
            newlikeobj= Like.objects.create(
            likedbyuser=user,
            dislikes=1,
            post=post
            )
            newlikeobj.save()
            return Response({'Message':f"You disliked the post {post.title}"},status=status.HTTP_201_CREATED) 
        else:
            if likeobj.dislikes==1:
                return Response({'Message':"You have already disliked the post"},status=status.HTTP_403_FORBIDDEN)
            else:
                likeobj.dislikes=1
                likeobj.likes=0
                likeobj.save()
                return Response({'Message':f"You dislikeliked the post {post.title}"},status=status.HTTP_201_CREATED)





class AddCommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,id):
        user =User.objects.get(username=request.user.username)
        try:
            post =Post.objects.get(id=id)
        except:
            return Response({'Message':"Post doesnt exist"},status=status.HTTP_404_NOT_FOUND)
       
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            new_comment = Comment.objects.create(
            commentedbyuser=user,
            post=post,
            content=request.data['content']
        )
            new_comment.save()
            return Response({'Comment_id':new_comment.id,"content":serializer.data['content']},status=status.HTTP_201_CREATED)

        else :
            return Response({'status':404,'message':"Something went wrong"}) 




class post(APIView):
    
    permission_classes = (IsAuthenticated,)
    def get(self,request,id):
        try:
            post =Post.objects.get(id=id)
        except:
            return Response({'Message':"Post doesnt exist"},status=status.HTTP_404_NOT_FOUND)

        Likes= post.likes.all()
        # print(Likes[0)
        likecount=0
        dislikecount=0
        for like in Likes:
            if like.likes==1:
                likecount+=1
            elif like.dislikes==1:
                dislikecount+=1
        serializer=PostSerializer(post)
        return Response({'Post':serializer.data,'Likes':likecount,"Dislikes":dislikecount},status=status.HTTP_200_OK)


class AllPosts(APIView):
    
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        try:
            post =Post.objects.all()
        except:
            return Response({'Message':" No Post exist"},status=status.HTTP_404_NOT_FOUND)

        serializer=AllPostSerializer(post,many=True)
        return Response({'Post':serializer.data},status=status.HTTP_200_OK)