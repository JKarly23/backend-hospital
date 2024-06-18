from core.apps.permission import IsAdminOrReadOnly
from .serializer import NurseSerializer
from ..models import Nurse
from rest_framework.viewsets import ModelViewSet

class NurseMVS(ModelViewSet):

    serializer_class = NurseSerializer
    queryset = Nurse.objects.all()
    permission_classes = [IsAdminOrReadOnly]

