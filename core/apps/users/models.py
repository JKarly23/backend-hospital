from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username,first_name,last_name,email,date_of_birth,gender,address,phone_number,image,user_type='patients',password=None):
        if not email:
            raise ValueError('The user must have an email')
        
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            phone_number=phone_number,
            image=image,
            user_type=user_type
        )

        user.set_password(password)
        user.save()
        return user





class CustomizerAccount(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=[('male','Male'),('female','Female')], max_length=50)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=10)
    image = models.ImageField(upload_to='img/')
    user_type = models.CharField(choices=[('nurses','Nurses'),('doctors','Doctors'),('patients','Patients'), default='patients'], max_length=50)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name','email','gender','address','phone_number']

    def __str__(self):
        return f"Username: {self.username}"
    
    def has_perm(self,perm, obj=None):
        return True

    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_staff