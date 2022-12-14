
from django.urls import path
from .views import login,follow,unfollow,userprofile,PostAPIView,DeletePostAPIView,LikeAPIView,DislikeAPIView,AddCommentAPIView,post,AllPosts

urlpatterns = [
    path('login/', login.as_view(), name='login'),
    path("follow/<str:id>", follow.as_view(), name="follow"),
    path("unfollow/<str:id>", unfollow.as_view(), name="unfollow"),
    path("userprofile", userprofile.as_view(), name="userprofile"),
    path("addpost",PostAPIView.as_view(), name="addpost"),
    path("deletepost/<int:id>",DeletePostAPIView.as_view(), name="deletepost"),
    path("likepost/<int:id>",LikeAPIView.as_view(), name="likepost"),
    path("dislikepost/<int:id>",DislikeAPIView.as_view(), name="dislikepost"),
    path("addcomment/<int:id>", AddCommentAPIView.as_view(), name="addcomment"),
    path("post/<int:id>", post.as_view(), name="post"),
    path("all_post/", AllPosts.as_view(), name="post"),
]


