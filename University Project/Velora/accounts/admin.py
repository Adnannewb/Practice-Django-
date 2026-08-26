from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "created_at")
    list_filter = ("role", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        ("Velora profile", {"fields": ("role", "phone", "avatar", "bio")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Velora profile", {"fields": ("email", "role", "phone")}),
    )
