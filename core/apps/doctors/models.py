from django.db import models
from core.apps.users.models import CustomAccount

# Create your models here.
class Doctor(models.Model):
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE, related_name='user_doctor')
    specialty = models.CharField(max_length=50)
    years_experience = models.IntegerField()
    
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

    