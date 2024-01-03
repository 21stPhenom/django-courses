from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', obtain_auth_token, name='login'),
]