from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.


# Go to the BaseUserAdmin code and extract add_fields set to your class to add fields
# it's the only way to extend the base user model
# When ever you are using the user fields on any app don't import the app directly use setting.AUTH_USER_MODEL from django.conf settings

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2",'email','first_name','last_name'),
            },
        ),
    )
