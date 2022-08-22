from django.urls import path
from user.views import HelloAPI, RegisterAPI ,LogoutView, LogoutAllView,LoginView

urlpatterns = [
    path(r'login/', LoginView.as_view(), name='knox_login'),
    path(r'logout/', LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', LogoutAllView.as_view(), name='knox_logoutall'),

    path('register/', RegisterAPI.as_view(), name='UserRegister'),
    path('hello/', HelloAPI.as_view(), name='f'),
]