from django.contrib import admin
from .models import UserProfile, Topic, Explanation, UserVote, UserFavorite
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


admin.site.register(UserProfile)
admin.site.register(Topic)
admin.site.register(Explanation)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
