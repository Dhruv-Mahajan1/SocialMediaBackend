from django.contrib import admin
from .models import User,Following,Like,Comment,Post
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Following)
