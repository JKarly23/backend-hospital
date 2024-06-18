from django.db import models

from core.apps.doctors.models import Doctor
from core.apps.patients.models import Patient

# Create your models here.
class Appointment(models.Model):
    consultation_date = models.DateTimeField(auto_now_add=True)
    reason_of_visit = models.TextField()
    symptoms =models.TextField()
    diagnosis = models.TextField()
    prescribed_treatament = models.TextField()
    observation = models.TextField()
    test_conducted = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.patient.user.first_name} {self.doctor.user.first_name} {self.reason_of_visit}"


