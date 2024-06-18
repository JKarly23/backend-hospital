from rest_framework.serializers import ModelSerializer
from ..models import Nurse

class NurseSerializer(ModelSerializer):

    class Meta:
        model = Nurse
        fields = "__all__"
    
