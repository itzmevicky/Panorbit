from .utils import otp
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, otp_code=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set!")
        
        email = self.normalize_email(email)
        user = self.model(email=email, otp_code=otp_code, **extra_fields)
        user.set_unusable_password()  # Set an unusable password
        user.save()
        return user
    
    def create_superuser(self, email, otp_code=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, otp_code=otp_code, **extra_fields)

class CustomUser(AbstractBaseUser):
    class Meta:
       db_table = 'CustomUser'
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    email = models.EmailField(primary_key=True)
    phone_number = models.CharField(max_length=20)
    otp_code = models.CharField(max_length=6)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'phone_number']


