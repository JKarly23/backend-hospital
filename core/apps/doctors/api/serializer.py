from rest_framework.serializers import ModelSerializer
from ..models import Doctor

class DoctorSerializer(ModelSerializer):

    class Meta:
        model = Doctor
        fields = "__all__"
    
