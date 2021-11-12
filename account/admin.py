from django.contrib import admin
from .models import UserProfile, Follow
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'organizer', 'is_verified'
    ]


class FollowAdmin(admin.ModelAdmin):
    list_display = [
        'from_user',
        'to_user',
        'followed'
    ]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Follow, FollowAdmin)
