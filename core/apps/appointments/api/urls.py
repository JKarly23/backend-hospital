from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .controller import AppointmentMVS,display_appointments,appointments_request

router = DefaultRouter()
router.register(r"",AppointmentMVS,basename="appointments")

urlpatterns = [
    path("appointments/",include(router.urls)),
    path("patient/<int:pk>/appointments/",display_appointments, name="appointment_patient"),
    path("request/appointment/",appointments_request, name="appointments_request"),
]
