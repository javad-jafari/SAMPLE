from django.urls import path
from password.views import ChangePasswordView, ForgetPassword

urlpatterns = [
    path('change/', ChangePasswordView.as_view(), name="change-password"),
    path('forget/<str:pk>/', ForgetPassword.as_view(), name="forget-password"),
]
