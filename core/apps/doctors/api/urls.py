from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .controller import DoctorsMVS

router = DefaultRouter()
router.register(r"", DoctorsMVS, basename="doctors")

urlpatterns = [
    path("doctors/",include(router.urls))
]
