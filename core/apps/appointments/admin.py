from django.contrib import admin
from .models import Appointment
from .models import AceptedRequest    
from .models import CanceledRequest
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'consultation_date', 'get_patient_name', 'get_doctor_name', 'reason_of_visit', 'diagnosis')
    list_filter = ('consultation_date', 'doctor__user__first_name')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    ordering = ('-consultation_date',)

    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}"
    get_patient_name.short_description = 'Patient'

    def get_doctor_name(self, obj):
        return f"{obj.doctor.user.first_name} {obj.doctor.user.last_name}"
    get_doctor_name.short_description = 'Doctor'

    def status(self, obj):
        return obj.status  # Replace with actual status field if defined

    status.short_description = 'Status'


@admin.register(AceptedRequest)
class AcceptedRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'reason', 'proposed_date', 'doctor')
    list_filter = ('proposed_date',)
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    readonly_fields = ('proposed_date',)
    date_hierarchy = 'proposed_date'




@admin.register(CanceledRequest)
class CanceledRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'message')
    search_fields = ('patient__user__first_name', 'patient__user__last_name')
