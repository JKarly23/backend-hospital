from datetime import timedelta, timezone
import random
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from core.apps.doctors.models import Doctor
from .serializer import AppointmentSerializer
from ..models import Appointment, AceptedRequest, CanceledRequest
from core.apps.permission import IsDoctorOrReadOnly, IsPatient
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_list_or_404
from django.core.mail import send_mail

class AppointmentMVS(ModelViewSet):

    queryset = Appointment.objects.all()
    permission_classes = [IsDoctorOrReadOnly]
    serializer_class = AppointmentSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().list(request, *args, **kwargs)
        elif request.user.user_type == "doctors":
            list_appointments = Appointment.objects.filter(doctor=request.user)
        else:
            raise PermissionDenied(
                "You not have permission for look this datas")

        serializer = self.serializer_class(list_appointments, many=True)
        return Response(serializer.data)


@api_view(["GET",])
def display_appointments(request, pk):
    list_appointments = get_list_or_404(Appointment, patient=pk)
    if not list_appointments:
        return Response({"Info": "This patient not have appointment registred"})
    serializer = AppointmentSerializer(list_appointments, many=True)
    return Response(serializer.data)


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
