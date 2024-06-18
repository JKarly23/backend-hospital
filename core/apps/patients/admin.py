from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ClinicHistory, Patient
from core.apps.doctors.models import Doctor
from core.apps.nurses.models import Nurse

# Admin for ClinicHistory
from django.contrib import admin
from .models import ClinicHistory

class ClinicHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_modifed', 'get_doctors', 'get_nurses')
    search_fields = ('diseases', 'treatments')
    list_filter = ('last_modifed',)
    ordering = ('-last_modifed',)
    filter_horizontal = ('doctor', 'enfermera')

    def get_doctors(self, obj):
        return ", ".join([f"{doctor.user.first_name} {doctor.user.last_name}" for doctor in obj.doctor.all()])
    get_doctors.short_description = 'Doctors'

    def get_nurses(self, obj):
        return ", ".join([f"{nurse.user.first_name} {nurse.user.last_name}" for nurse in obj.enfermera.all()])
    get_nurses.short_description = 'Nurses'



# Admin for Patient
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'get_clinic_history', 'get_doctors', 'get_nurses')
    search_fields = ('user__email',)
    list_filter = ('user__date_joined',)
    ordering = ('-user__date_joined',)
    filter_horizontal = ('doctor', 'nurse')

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'

    def get_clinic_history(self, obj):
        return obj.clinic_history.id
    get_clinic_history.short_description = 'Clinic History'

    def get_doctors(self, obj):
        return ", ".join([f"{doctor.user.first_name} {doctor.user.last_name}" for doctor in obj.doctor.all()])
    get_doctors.short_description = 'Doctors'

    def get_nurses(self, obj):
        return ", ".join([f"{nurse.user.first_name} {nurse.user.last_name}"  for nurse in obj.nurse.all()])
    get_nurses.short_description = 'Nurses'

# Registering models to the admin site
admin.site.register(ClinicHistory, ClinicHistoryAdmin)
admin.site.register(Patient, PatientAdmin)
