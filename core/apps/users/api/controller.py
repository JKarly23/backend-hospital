from django.http import Http404
from core.apps.users.models import CustomAccount
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer


class UserModelVS(ModelViewSet):

    permission_classes = [IsAdminUser]
    queryset = CustomAccount.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data 
        try:
            user = CustomAccount.objects.create_superuser(**data)
            user.save()
        except CustomAccount.DoesNotExist as e:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)


    