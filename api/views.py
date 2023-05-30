import pyotp
from .serializers import *
from django.urls import reverse
from rest_framework import generics
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings





class UserRegistration(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            return Response("User with the same email already exists. Please Login", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("Account Successfully Created", status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save()
        return user

class LoginVerify(generics.CreateAPIView):
    serializer_class = LoginSerializer      
    def post(self, request, *args, **kwargs):       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        try:
            user = authenticate(request, email=email, otp=otp)
            if user: 
                login(request, user)     
                return Response('OTP Validated',status=status.HTTP_200_OK)
            return Response('Invalid OTP',status=status.HTTP_401_UNAUTHORIZED)
        except Exception as ex:
            return Response("Something Wrong",status=400)

class Home(generics.ListAPIView):
    permission_classes =  [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user   
        data = {
            'message': f'Welcome {user}',
        }     
        return Response(data)

class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

class Logout(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse('login'))
            
class GenertateOTP(generics.CreateAPIView):
    serializer_class = OTPGenerate
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        try :
            user = self.serializer_class.Meta.model.objects.get(email=email)
            if not user:
                return Response("User Don't Exist")
            otp = pyotp.TOTP(pyotp.random_base32(), digits=6).now()
            user.otp = otp
            self.sendMail(email,otp)
            user.save()
            return Response(f'OTP has been Emailed on {email} Please Check.')            
        except Exception as ex:
            print(ex)
            return Response("Something Wrong.....")

    def sendMail(self,email,otp):
        subject = 'OTP Verfication'
        message = f'Heya Your OTP is {otp} Please Login Using OTP.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
