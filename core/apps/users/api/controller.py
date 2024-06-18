from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from core.apps.doctors.models import Doctor
from core.apps.nurses.models import Nurse
from core.apps.patients.models import Patient
from core.apps.users.models import CustomAccount
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView


class UserModelVS(ModelViewSet):

    permission_classes = [IsAdminUser]
    queryset = CustomAccount.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data 
        try:
            user = CustomAccount.objects.create_superuser(**data)
            user.save()
        except CustomAccount.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)



#Por si al bestia se le ocurre hacer el registro de la otra forma

class UserAPV(APIView):

    @permission_classes([IsAdminUser])
    def post(self, request):
        datas = {}
        user_type = request.data.get('user_type')
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                
                user = CustomAccount.objects.create(
                    username=serializer.validated_data['username'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'],
                    date_of_birth=serializer.validated_data['date_of_birth'],
                    gender=serializer.validated_data['gender'],
                    address=serializer.validated_data['address'],
                    phone_number=serializer.validated_data['phone_number'],
                    image=serializer.validated_data['image'],
                    user_type=user_type
                )
                user.set_password(request.data.get('password'))
                user.save()
                datas['user'] = UserSerializer(user).data
                datas["message"] = f"{user_type.capitalize()} created successfully"
            except ValidationError as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

          
            if user_type == "patients":
                try:
                    username_doctor = request.data.get("doctor")
                    username_nurse = request.data.get("nurse")
                    datas["doctor"] = username_doctor
                    datas["nurse"] = username_nurse

                    user_doctor = get_object_or_404(CustomAccount, username=username_doctor, user_type='doctors')
                    doctor = get_object_or_404(Doctor, user=user_doctor)
                    user_nurse = get_object_or_404(CustomAccount, username=username_nurse, user_type='nurses')
                    nurse = get_object_or_404(Nurse, user=user_nurse)
                    
                    patient = Patient.objects.create(user=user)
                    patient.doctor.add(doctor)
                    patient.nurse.add(nurse)
                    patient.save()
                except Exception as e:
                    return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            elif user_type == "doctors":
                try:
                    specialty = request.data.get("specialty")
                    years_experience = request.data.get("years_experience")
                    doctor = Doctor.objects.create(user=user, specialty=specialty, years_experience=years_experience)
                    doctor.save()
                except Exception as e:
                    return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            elif user_type == "nurses":
                try:
                    categoria = request.data.get("categoria")
                    nurse = Nurse.objects.create(user=user, categoria=categoria)
                    nurse.save()
                except Exception as e:
                    return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(datas, status=status.HTTP_201_CREATED)
