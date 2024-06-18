from django.forms import ValidationError
from core.apps.doctors.models import Doctor
from core.apps.nurses.models import Nurse
from core.apps.permission import IsAdminOrReadOnly, IsDoctorOrReadOnly
from core.apps.users.api.serializer import UserSerializer
from core.apps.users.models import CustomAccount
from .serializer import PatientsSerializer, ClinicHistorySerializer
from ..models import Patient, ClinicHistory
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


class PatientMVS(ModelViewSet):

    serializer_class = PatientsSerializer
    queryset = Patient.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
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
                username_doctor = self.request.data.get("doctor")
                username_nurse = self.request.data.get("nurse")
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


    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().list(request, *args, **kwargs)
            elif request.user.user_type == 'doctor':
                patients = Patient.objects.filter(doctor=request.user.doctor)
            elif request.user.user_type == 'nurse':
                patients = Patient.objects.filter(nurse=request.user.nurse)
            else:
                raise PermissionDenied(
                    "You don't have permission to view these records.")

            serializer = PatientsSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied(
                "You need to be authenticated to view these records.")


class ClinicHistoryMVS(ModelViewSet):

    serializer_class = ClinicHistorySerializer
    queryset = ClinicHistory.objects.all()
    permission_classes = [IsDoctorOrReadOnly]

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().list(request, *args, **kwargs)
            elif request.user.user_type == 'doctor':
                clinic_history = ClinicHistory.objects.filter(
                    doctor=request.user.doctor)
            elif request.user.user_type == 'nurse':
                clinic_history = ClinicHistory.objects.filter(
                    nurse=request.user.nurse)
            else:
                raise PermissionDenied(
                    "You don't have permission to view these records.")

            serializer = ClinicHistorySerializer(clinic_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied(
                "You need to be authenticated to view these records.")


@api_view(["GET",])
def display_medical(request, pk):
    clinical_history = get_object_or_404(ClinicHistory,patient=pk)
    if not clinical_history:
        return ValueError("This patient does not have a medical history, you have to do a clinical history")
    serializer = ClinicHistorySerializer(clinical_history)
    return Response(serializer.data)
