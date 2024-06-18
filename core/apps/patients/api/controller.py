import datetime
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

class ClinicHistoryMVS(ModelViewSet):

    serializer_class = ClinicHistorySerializer
    queryset = ClinicHistory.objects.all()
    permission_classes = [IsDoctorOrReadOnly]

    """ def perform_create(self, serializer):
        try:
            last_modified = serializer.validated_data.get('last_modified')
            today = datetime.now().date()
            if (today - last_modified).days / 365 >= 5:
                username_doctor = self.request.data.get("doctor")
                username_nurse = self.request.data.get("nurse")
                username_patient = self.request.data.get("patient")

                user_doctor = get_object_or_404(CustomAccount, username=username_doctor, user_type='doctors')
                doctor = get_object_or_404(Doctor, user=user_doctor)
                user_nurse = get_object_or_404(CustomAccount, username=username_nurse, user_type='nurses')
                nurse = get_object_or_404(Nurse, user=user_nurse)
                user_patient = get_object_or_404(CustomAccount, username=username_patient, user_type='patients')
                patient = get_object_or_404(Patient, user=user_patient, user_type='patients')


                clinic_history = ClinicHistory.objects.create(
                    treatments=serializer.validated_data.get("treatments"),
                    diseases=serializer.validated_data.get("diseases")
                )
                clinic_history.doctor.add(doctor)
                clinic_history.enfermera.add(nurse)
                clinic_history.patient = patient
                clinic_history.save()

                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "To create a new medical history, a minimum of 5 years must have passed since its last modification."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST) """


    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                clinic_history = self.get_queryset()
            elif request.user.user_type == 'doctor':
                clinic_history = ClinicHistory.objects.filter(
                    doctor=request.user.doctor)
            elif request.user.user_type == 'nurse':
                clinic_history = ClinicHistory.objects.filter(
                    enfermera=request.user.nurse)
            else:
                raise PermissionDenied(
                    "You don't have permission to view these records."
                )

            data = []
            for history in clinic_history:
                try:
                    # Obtener detalles del paciente
                    patient_user = CustomAccount.objects.get(id=history.patient.user.id)
                    
                    # Obtener nombres completos de los doctores y enfermeras
                    doctor_names = [f"{doctor.user.first_name} {doctor.user.last_name}" for doctor in history.doctor.all()]
                    nurse_names = [f"{nurse.user.first_name} {nurse.user.last_name}" for nurse in history.enfermera.all()]

                    history_data = {
                        'clinic history': history.id,
                        'last_modified': history.last_modifed,
                        'treatments': history.treatments,
                        'diseases': history.diseases,
                        'patient': {
                            'id': patient_user.id,
                            'username': patient_user.username,
                            'first_name': patient_user.first_name,
                            'last_name': patient_user.last_name,
                            'email': patient_user.email,
                            'phone_number': patient_user.phone_number,
                            'image': patient_user.image.url if patient_user.image else None,
                        },
                        'doctor': doctor_names,
                        'nurse': nurse_names,
                    }
                    data.append(history_data)
                except Exception as e:
                    return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied(
                "You need to be authenticated to view these records."
            )


@api_view(["GET",])
def display_medical(request, pk):
    clinical_history = get_object_or_404(ClinicHistory,patient=pk)
    if not clinical_history:
        return ValueError("This patient does not have a medical history, you have to do a clinical history")
    serializer = ClinicHistorySerializer(clinical_history)
    return Response(serializer.data)



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

                clinic_history = ClinicHistory.objects.create(
                    patient=patient,
                    treatments="Initial Treatment",  
                    diseases="Initial Diseases"  
                )
                clinic_history.doctor.add(doctor)
                clinic_history.enfermera.add(nurse)
                clinic_history.save()
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                patients = self.get_queryset()
            elif request.user.user_type == 'doctor':
                patients = Patient.objects.filter(doctor=request.user.doctor)
            elif request.user.user_type == 'nurse':
                patients = Patient.objects.filter(nurse=request.user.nurse)
            else:
                raise PermissionDenied(
                    "You don't have permission to view these records."
                )

            data = []
            for patient in patients:
                try:
                    user = CustomAccount.objects.get(id=patient.user.id)
                    
                    doctor_names = ", ".join([f"{doc.user.first_name} {doc.user.last_name}" for doc in patient.doctor.all()])
                    nurse_names = ", ".join([f"{nur.user.first_name} {nur.user.last_name}" for nur in patient.nurse.all()])
                    
                    patient_data = {
                        'patient': patient.id,
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'phone_number': user.phone_number,
                            'image': user.image.url if user.image else None,
                        },
                        'doctors': doctor_names,
                        'nurses': nurse_names,
                       
                    }
                    data.append(patient_data)
                except Exception as e:
                    return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied(
                "You need to be authenticated to view these records."
            )