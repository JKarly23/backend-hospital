from core.apps.permission import IsAdminOrReadOnly
from .serializer import DoctorSerializer
from ..models import Doctor
from rest_framework.viewsets import ModelViewSet

class DoctorsMVS(ModelViewSet):

    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    permission_classes = [IsAdminOrReadOnly]


