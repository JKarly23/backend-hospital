from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .controller import UserModelVS
router = DefaultRouter()
router.register(r'users',UserModelVS, basename='users')

urlpatterns = [
    path('',include(router.urls))
]
