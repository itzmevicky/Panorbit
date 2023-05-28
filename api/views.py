import pyotp
from .serializers import *
from django.urls import reverse
from rest_framework import generics
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout



class UserRegistration(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        if user:
            return Response("Account Successfully Created",status=201)
        return Response("Something Wrong",status=400)

    def perform_create(self, serializer):
        user = serializer.save()
        user.save()
        return user

class LoginVerify(generics.CreateAPIView):
    serializer_class = LoginSerializer   
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('Home'))
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        try:
            user = authenticate(request, email=email, otp=otp)
            if user: 
                login(request, user)              
                return redirect(reverse('home'))
            return Response('Invalid OTP',status=400)
        except Exception as ex:
            return Response("Something Wrong",status=400)

class Home(generics.ListAPIView):
    permission_classes =  [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user        
        return Response(f'Welcome {user}')

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
            otp = pyotp.TOTP(pyotp.random_base32(), digits=6).now()
            user.otp = otp
            #mail the otp to user
            user.save()
            return Response('OTP has been Emailed Please Check')            
        except Exception as ex:
            return Response("User Don't Exist")