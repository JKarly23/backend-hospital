from rest_framework. serializers import ModelSerializer
from ..models import Appointment, AceptedRequest, CanceledRequest


class AppointmentSerializer(ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"


class AceptedRequestSerializer(ModelSerializer):

    class Meta:
        model = AceptedRequest
        fields = "__all__"


class CanceledRequest:
    class Meta:
        model = CanceledRequest
        fields = "__all__"
