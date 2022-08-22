from django.urls import path

from otp.views import SendOTPAPI,VerifyOTPAPI



urlpatterns = [

    path('sendOTP/', SendOTPAPI.as_view(), name='sendOTP'),
    path('verifyOTP/', VerifyOTPAPI.as_view(), name='verifyOTP'),


]