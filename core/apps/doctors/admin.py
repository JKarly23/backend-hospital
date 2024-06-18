from django.contrib import admin
from .models import Doctor

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'specialty', 'years_experience', 'get_email')
    search_fields = ('user__first_name', 'user__last_name', 'specialty')
    list_filter = ('specialty', 'years_experience')
    ordering = ('-years_experience',)

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Doctor Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(Doctor, DoctorAdmin)
