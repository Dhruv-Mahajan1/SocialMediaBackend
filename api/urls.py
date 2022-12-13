
from django.urls import path
from .views import login,follow,unfollow,userprofile

urlpatterns = [
    path('login/', login.as_view(), name='login'),
    path("follow/<str:id>", follow.as_view(), name="follow"),
    path("unfollow/<str:id>", unfollow.as_view(), name="unfollow"),
    path("userprofile", userprofile.as_view(), name="userprofile"),
    # path("post-comment/<str:action>", views.post_comment, name="post-comment"),
    
    # path("edit-profile", views.edit_profile, name="edit-profile"),
    # path("following", views.following, name="following"),
    
    # path("like/<str:action>/<int:action_id>", views.like, name="like"),
]


