from django.urls import path

from otp.views import SendOTPAPI



urlpatterns = [

    path('sendOTP/', SendOTPAPI.as_view(), name='sendOTP'),

]