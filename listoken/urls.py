from django.urls import path

from listoken.views import DeleteTokenAPI, ListTokenAPI



urlpatterns = [

    path('', ListTokenAPI.as_view(), name='list_user_token'),
    path('<str:digest>/', DeleteTokenAPI.as_view(), name='del_user_token'),



]