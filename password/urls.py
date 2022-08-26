from django.urls import path
from password.views import ChangePasswordView

urlpatterns = [
    path('change/', ChangePasswordView.as_view(), name="change-password"),
]
