from django.contrib import admin
from .models import MerchantUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'id', 'is_staff', 'is_active', 'created_at']
    list_filter = ["is_superuser"]
    fieldsets = [
        ('User credintials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["is_active"]}),
        ("Permissions", {"fields": ["is_superuser"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(MerchantUser,UserAdmin)