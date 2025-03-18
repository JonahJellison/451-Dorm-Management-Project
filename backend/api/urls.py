from django.urls import path, include
from api import views


urlpatterns = [
    path('api/register/', views.register_user, name='user-register'),
    path('api/login/', views.login_user, name='login-user'),
]
