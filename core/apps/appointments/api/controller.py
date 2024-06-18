from rest_framework.viewsets import ModelViewSet

from .serializer import AppointmentSerializer
from ..models import Appointment
from core.apps.permission import IsDoctorOrReadOnly

class AppointmentMVS(ModelViewSet):

    queryset = Appointment.objects.all()
    permission_classes = [IsDoctorOrReadOnly]
    serializer_class = AppointmentSerializer