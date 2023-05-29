from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserProfileManager(BaseUserManager):
    def _create_user(self, email, otp=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = email  # Set the username to be the same as the email
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('username', username)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.otp = otp
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, otp=None, password=None, **extra_fields):
        return self._create_user(email, otp, password, **extra_fields)

    def create_superuser(self, email, otp=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, otp, password, **extra_fields)

class CustomUser(AbstractUser):
    class Meta:
        db_table = "custom_user"

    # Additional fields for UserProfile
    GENDER_CHOICES = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('OTHER', 'OTHER')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    email = models.EmailField(primary_key=True)
    phone = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'phone']

    def save(self, *args, **kwargs):
        # Set the username to be the same as the email
        self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name

