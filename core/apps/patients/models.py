from django.db import models
from core.apps.doctors.models import Doctor
from core.apps.nurses.models import Nurse
from core.apps.users.models import CustomAccount

# Create your models here.
class ClinicHistory(models.Model):
   
    last_modifed = models.DateTimeField(auto_now_add=False)
    treatments = models.TextField()
    diseases = models.TextField()
    doctor = models.ManyToManyField(Doctor)
    enfermera = models.ManyToManyField(Nurse)

class Patient(models.Model):
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE, related_name='user_patient')
    clinic_history = models.OneToOneField(ClinicHistory, on_delete=models.CASCADE, related_name="clinic_history")
    doctor = models.ManyToManyField(Doctor)
    nurse = models.ManyToManyField(Nurse)