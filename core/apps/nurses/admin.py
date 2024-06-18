from django.contrib import admin
from .models import Nurse

class NurseAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'categoria', 'get_email')
    search_fields = ('user__first_name', 'user__last_name', 'categoria')
    list_filter = ('categoria',)
    ordering = ('user__last_name',)

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Nurse Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(Nurse, NurseAdmin)
