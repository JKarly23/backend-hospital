from core.apps.permission import IsAdminOrReadOnly, IsDoctorOrReadOnly
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
    clinical_history = get_object_or_404(ClinicHistory, id=pk)
    serializer = ClinicHistorySerializer(clinical_history)
    return Response(serializer.data)
