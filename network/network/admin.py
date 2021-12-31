from django.contrib import admin
from .models import User, Post, Profile

class UserAdmin(admin.ModelAdmin):
    list_display=("username", "email")

class PostAdmin(admin.ModelAdmin):
    list_display=("post_owner", "message", "love", "timestamp")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile)