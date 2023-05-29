from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistration.as_view(),name='register'),
    path('login/', LoginVerify.as_view(),name='login'),
    path('home/', Home.as_view(),name='home'),
    path('genOTP/',GenertateOTP.as_view()),
    path('logout/',Logout.as_view())
]
