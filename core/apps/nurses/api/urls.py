from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .controller import NurseMVS

router = DefaultRouter()
router.register(r"",NurseMVS,basename="nurses")

urlpatterns = [
    path('nurses/',include(router.urls))
]
