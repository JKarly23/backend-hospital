from rest_framework.serializers import ModelSerializer
from core.apps.users.models import CustomAccount

class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomAccount
        exclude = ['is_admin','is_active','is_staff','is_superuser','user_type']
