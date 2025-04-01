from django.urls import path, include
from api import views


urlpatterns = [
    path('register', views.register_user, name='user-register'),
    path('login', views.login_user, name='login-user'),
    path('fetch_dormroom_data', views.fetch_dormroom_data, name='fetch_dormroom_data'),
    path('book_room', views.book_room, name='book_room'),
    path('fetch_admin_data', views.fetch_admin_data, name='fetch_admin_data'),
]
