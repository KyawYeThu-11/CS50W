from django.contrib import admin
from .models import User, Link, Message

class UserAdmin(admin.ModelAdmin):
    list_display=("username", "email", "subscribe", "time_interval", "receiving_date")

class LinkAdmin(admin.ModelAdmin):
    list_display=("name", "url", "description", "category", "source", "date")

class MessageAdmin(admin.ModelAdmin):
    list_display=("creator", "message")

admin.site.register(User, UserAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Message, MessageAdmin)
