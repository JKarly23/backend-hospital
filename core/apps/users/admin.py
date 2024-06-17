from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomAccount

class CustomAccountAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'user_type','thumbnail')
    list_filter = ('gender', 'user_type', 'is_active', 'is_staff', 'is_admin', 'is_superuser', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'thumbnail')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'address', 'phone_number', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        ('Dates', {'fields': ('date_joined', 'last_login')}),
        ('User Type', {'fields': ('user_type',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'gender', 'address', 'phone_number', 'image', 'password1', 'password2', 'user_type', 'is_active', 'is_staff', 'is_admin', 'is_superuser'),
        }),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return ''
    thumbnail.short_description = 'Profile Image'

    filter_horizontal = ()

# Registra el modelo con la clase Admin personalizada
admin.site.register(CustomAccount, CustomAccountAdmin)
