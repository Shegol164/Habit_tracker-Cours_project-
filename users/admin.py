from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'telegram_chat_id', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {'fields': ('telegram_chat_id',)}),
    )