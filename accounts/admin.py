from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# User manegement UI Components (Built on Djangos UserAdmin pre-built pages)
class CustomUserAdmin(UserAdmin):
    # Use our custom user model to use email for login and set roles
    model = CustomUser

    # User list page
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')

    # Default sort order (trailing ',' for python tuple)
    ordering = ('email',)

    # EDIT forms for existing users
    # (<Section Name>, {'fields': (<modelProperty1>, <modelProperty2>)})
    fieldsets = (
        # Login form (not sure how this is an edit form but that's Django apparently)
        (None, {
            "fields": (
                'email',
                'password'
            ),
        }),
        # Personal info form
        ('Personal Info', {
            "fields": (
                'first_name',
                'last_name',
                'role'
            ),
        }),
        # Permissions form
        ('Permissions', {
            "fields": (
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )

    # CREATE forms for new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'role',
                'password1',
                'password2',
            ),
        }),
    )
    