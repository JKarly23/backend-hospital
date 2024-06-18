from django.db import models
from core.apps.users.models import CustomAccount

# Create your models here.
class Nurse(models.Model):
    user = models.ForeignKey(CustomAccount, on_delete=models.CASCADE,related_name='user_nurse')
    categoria =models.CharField(choices=[('licenciada','Licenciada'),('tecnica','Tecnica')], max_length=50, default='licenciada')

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"