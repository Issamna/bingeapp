from django.contrib import admin
from .models import User, UserProfile


class UserProfileInLine(admin.TabularInline):
    model = UserProfile
    extra = 0
    can_delete = False
    max_num = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")
    search_fields = ["email", "first_name", "last_name"]
    inlines = [UserProfileInLine]
    list_per_page = 25


admin.site.register(User, UserAdmin)