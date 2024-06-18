from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .controller import PatientMVS, ClinicHistoryMVS,display_medical

router = DefaultRouter()
router1 = DefaultRouter()
router.register(r"",PatientMVS, basename="patients")
router1.register(r"", ClinicHistoryMVS, basename="history")

urlpatterns = [
    path("patients/", include(router.urls)),
    path("history/", include(router1.urls)),
    path('patient/<int:pk>/history/',display_medical, name="show_medical_history"),
]
