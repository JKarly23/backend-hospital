from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .controller import PatientMVS, ClinicHistoryMVS

router = DefaultRouter()
router1 = DefaultRouter()
router.register(r"",PatientMVS, basename="patients")
router1.register(r"", ClinicHistoryMVS, basename="history")

urlpatterns = [
    path("patients/", include(router.urls)),
    path("history/", include(router1.urls)),
]
