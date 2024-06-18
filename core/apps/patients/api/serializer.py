from rest_framework.serializers import ModelSerializer
from core.apps.patients.models import Patient,ClinicHistory

class PatientsSerializer(ModelSerializer):

    class Meta:
        model = Patient
        fields = "__all__"
    
class ClinicHistorySerializer(ModelSerializer):

    class Meta:
        model = ClinicHistory
        fields = "__all__"