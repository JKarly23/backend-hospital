from datetime import timedelta, timezone
import random
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from core.apps.doctors.models import Doctor
from core.apps.patients.models import Patient
from core.apps.users.models import CustomAccount
from .serializer import AceptedRequestSerializer, AppointmentSerializer
from ..models import Appointment, AceptedRequest, CanceledRequest
from core.apps.permission import IsDoctorOrReadOnly, IsPatient
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_list_or_404
from django.core.mail import send_mail
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser

class AppointmentMVS(ModelViewSet):

    queryset = Appointment.objects.all()
    permission_classes = [IsDoctorOrReadOnly]
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        doctor = self.request.user
        patient_user = get_object_or_404(CustomAccount,username=self.serializer_class.validated_data.get('patient'))
        patient = get_object_or_404(Patient,user=patient_user)

        serializer.save(
            consultation_date=serializer.validated_data.get('consultation_date'),
            reason_of_visit=serializer.validated_data.get('reason_of_visit'),
            symptoms=serializer.validated_data.get('symptoms'),
            diagnosis=serializer.validated_data.get('diagnosis'),
            prescribed_treatament=serializer.validated_data.get('prescribed_treatament'),
            observation=serializer.validated_data.get('observation'),
            test_conducted=serializer.validated_data.get('test_conducted'),
            patient=patient,
            doctor=doctor
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)




    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                queryset = self.get_queryset()
            elif request.user.user_type == "doctors":
                queryset = Appointment.objects.filter(doctor=request.user.doctor)
            else:
                raise PermissionDenied(
                    "You do not have permission to view these records."
                )

            data = []
            for appointment in queryset:
                patient_full_name = f"{appointment.patient.user.first_name} {appointment.patient.user.last_name}"
                doctor_full_name = f"{appointment.doctor.user.first_name} {appointment.doctor.user.last_name}"

                appointment_data = {
                    'id': appointment.id,
                    'consultation_date': appointment.consultation_date,
                    'reason_of_visit': appointment.reason_of_visit,
                    'symptoms': appointment.symptoms,
                    'diagnosis': appointment.diagnosis,
                    'prescribed_treatment': appointment.prescribed_treatament,
                    'observation': appointment.observation,
                    'test_conducted': appointment.test_conducted,
                    'patient': {
                        'id': appointment.patient.id,
                        'full_name': patient_full_name,
                    },
                    'doctor': {
                        'id': appointment.doctor.id,
                        'full_name': doctor_full_name,
                    }
                }
                data.append(appointment_data)

            return Response(data, status=status.HTTP_200_OK)

        else:
            raise PermissionDenied(
                "You need to be authenticated to view these records."
            )

@api_view(["GET",])
def display_appointments(request, pk):
    list_appointments = get_list_or_404(Appointment, patient=pk)
    if not list_appointments:
        return Response({"Info": "This patient not have appointment registred"})

    data = []
    for appointment in list_appointments:
                
        patient_full_name = f"{appointment.patient.user.first_name} {appointment.patient.user.last_name}"
        doctor_full_name = f"{appointment.doctor.user.first_name} {appointment.doctor.user.last_name}"

        appointment_data = {
            'id': appointment.id,
            'consultation_date': appointment.consultation_date,
            'reason_of_visit': appointment.reason_of_visit,
            'symptoms': appointment.symptoms,
            'diagnosis': appointment.diagnosis,
            'prescribed_treatment': appointment.prescribed_treatament,
            'observation': appointment.observation,
            'test_conducted': appointment.test_conducted,
            'patient': {
                'id': appointment.patient.id,
                'full_name': patient_full_name,
            },
            'doctor': {
                'id': appointment.doctor.id,
                'full_name': doctor_full_name,
            }
        }
        data.append(appointment_data)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST",])
@permission_classes([IsPatient]) 
def appointments_request(request):
    patient = request.user
    reason = request.data.get('reason')
    proposed_date = timezone.now() + timedelta(days=random.randint(1, 7))
    specialty = request.data.get('specialty')
    list_doctors = Doctor.objects.filter(specialty=specialty)
    if list_doctors:
        doctor = random.choice(list_doctors)
        AceptedRequest.objects.create(
            patient=patient,
            reason=reason,
            proposed_date=proposed_date,
            doctor=doctor
        )
        send_mail(
            'Medical Consultation Accepted',
            f'Your consultation request has been accepted. Date: {proposed_date}, Doctor: {doctor}',
            'perezsalcedocarlosjavier191@gmail.com',
            [request.user.email],
            fail_silently=False,
        )
        return Response({"message": "Consultation request accepted."}, status=200)
    else:
        CanceledRequest.objects.create(
            patient=patient,
            message=f"No doctors were found available with the specialty of {specialty}"
        )
        send_mail(
            'Canceled Medical Consultation',
            'Sorry, there are no doctors available to answer your question at this time.',
            'perezsalcedocarlosjavier191@gmail.com',
            [request.user.email],
            fail_silently=False,
        )
        return Response({"message": "Consultation cancelled, no doctors available."}, status=400)

@permission_classes([IsAdminUser])
@api_view(["GET"])
def display_request_accepted(request):
    queryset = AceptedRequest.objects.all()
    serializer = AceptedRequestSerializer(queryset, many=True)
    if serializer.is_valid():
        datas = {}
        doctor_user = get_object_or_404(CustomAccount,username=serializer.validated_data.get('doctor'))
        doctor = get_object_or_404(Doctor,user=doctor_user)
        patient_user = get_object_or_404(CustomAccount,username=serializer.validated_data.get('patient'))
        patient = get_object_or_404(Patient,user=patient_user)
        datas['doctor'] = f"{doctor.user.first_name} {doctor.user.last_name}"
        datas['patients'] = f"{patient.user.first_name} {patient.user.last_name}"
        datas['reason'] = serializer.validated_data.get("reason")
        datas['proposed_date'] = serializer.validated_data.get("proposed_date")
        return Response(datas, status=200)
    
    else:
        return Response(serializer.errors, status=400)
    
@permission_classes([IsAdminUser])
@api_view(["GET"])
def display_request_accepted(request):
    queryset = CanceledRequest.objects.all()
    serializer = AceptedRequestSerializer(queryset, many=True)
    if serializer.is_valid():
        datas = {}
        patient_user = get_object_or_404(CustomAccount,username=serializer.validated_data.get('patient'))
        patient = get_object_or_404(Patient,user=patient_user)
        datas['patients'] = f"{patient.user.first_name} {patient.user.last_name}"
        datas['message'] = serializer.validated_data.get("message")
        return Response(datas, status=200)
    else:
        return Response(serializer.errors, status=400)
