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
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="created on")



class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentedbyuser= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="commented by")
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="commented on")


class Like(models.Model):
    reactionchoices = [
        (0,"None"),
        (1, "like"),
        (2, "dislike"),
    ]
    id=models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    likedbyuser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="liked by")
    reaction = models.IntegerField(choices=reactionchoices, default=0)


    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"
        unique_together = [["likedbyuser", "post"]]

