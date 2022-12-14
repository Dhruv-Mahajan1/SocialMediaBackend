from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    userfollowed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers" )

    class Meta:
        verbose_name = "following"
        verbose_name_plural = "followings"
        unique_together = ['user', 'userfollowed']

    def __str__(self):
        return f"{self.userfollowed} followed by {self.user}"



class Post(models.Model):
    id=models.AutoField(primary_key=True)
    postedbyuser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="posted by")
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="created on")



class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments")
    commentedbyuser= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="commented by")
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="commented on")
    def __str__(self):
        return f"Comment -{self.content} made by {self.commentedbyuser} on {self.date.strftime('%d %b %Y %H:%M:%S')}"
   

class Like(models.Model):
    id=models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True,related_name="likes")
    likedbyuser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="liked by")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self): 
        like=""
        if self.likes==1:
            like="like"
        elif self.dislikes==1:
            like="dislike"
        return f"{like}- {self.id} by {self.likedbyuser}"

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"
        unique_together = [["likedbyuser", "post"]]

