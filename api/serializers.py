from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','gender','email','phone']



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    class Meta:
        fields = ['email','otp']

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name']

class OTPGenerate(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']