from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .controller import UserModelVS
router = DefaultRouter()
router.register(r'',UserModelVS, basename='users')

urlpatterns = [
    path('users/',include(router.urls)),
    #path("insert/user/",UserAPV.as_view(),name="insert_user")
]
