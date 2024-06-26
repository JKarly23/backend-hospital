from django.forms import ValidationError
from core.apps.permission import IsAdminOrReadOnly
from core.apps.users.api.serializer import UserSerializer
from core.apps.users.models import CustomAccount
from .serializer import DoctorSerializer
from ..models import Doctor
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

class DoctorsMVS(ModelViewSet):

    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    """def perform_create(self, serializer):
        datas = {}
        user_type = self.request.data.get('user_type')
        
        serializer_user = UserSerializer(data=self.request.data)
        if serializer_user.is_valid():
            try:
                user = CustomAccount.objects.create(
                    username=serializer_user.validated_data['username'],
                    first_name=serializer_user.validated_data['first_name'],
                    last_name=serializer_user.validated_data['last_name'],
                    email=serializer_user.validated_data['email'],
                    date_of_birth=serializer_user.validated_data['date_of_birth'],
                    gender=serializer_user.validated_data['gender'],
                    address=serializer_user.validated_data['address'],
                    phone_number=serializer_user.validated_data['phone_number'],
                    image=serializer_user.validated_data['image'],
                    user_type=user_type
                )
                user.set_password(self.request.data.get('password'))
                user.save()
                datas['user'] = UserSerializer(user).data
                datas["message"] = f"{user_type.capitalize()} created successfully"
            except ValidationError as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


            try:
                specialty = self.request.data.get("specialty")
                years_experience = self.request.data.get("years_experience")
                doctor = Doctor.objects.create(user=user, specialty=specialty, years_experience=years_experience)
                doctor.save()
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(datas, status=status.HTTP_201_CREATED)
        """
    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                doctors = self.get_queryset()
            else:
                raise PermissionDenied(
                    "You don't have permission to view these records."
                )

            data = []
            for doctor in doctors:
                try:
                    user = CustomAccount.objects.get(id=doctor.user.id)
                    
                    doctor_data = {
                        'doctor': doctor.id,
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'phone_number': user.phone_number,
                            'image': user.image.url if user.image else None,
                        },
                        'specialty': doctor.specialty,
                        'years_experience': doctor.years_experience,
                        # Include other doctor fields as needed
                    }
                    data.append(doctor_data)
                except Exception as e:
                    return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied(
                "You need to be authenticated to view these records."
            )