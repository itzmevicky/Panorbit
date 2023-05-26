

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from .utils import send_otp_email
import pyotp


class RegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        # Generate OTP
        otp = pyotp.TOTP(pyotp.random_base32(), digits=6).now()
        
        # Save user details with OTP
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        user = User.objects.create_user(username=email, email=email)
        userprofile = UserProfile(user=user, name=name, email=email, otp=otp)
        userprofile.save()
        
        # Send OTP to user's email

        send_otp_email(email, otp)