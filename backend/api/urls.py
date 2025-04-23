from django.urls import path, include
from api import views


urlpatterns = [
    path('register', views.register_user, name='user-register'),
    path('login', views.login_user, name='login-user'),
    path('fetch_dormroom_data', views.fetch_dormroom_data, name='fetch_dormroom_data'),
    path('book_room', views.book_room, name='book_room'),
    path('fetch_admin_data', views.fetch_admin_data, name='fetch_admin_data'),
    path('fetch_student_data',views.fetch_student_data,name='student_data_fetch'),
    path('student_info', views.student_info_view, name='student_info'),
    path('update_student_info',views.update_user_info,name='update_student_info'),
    path('maintenance_request', views.maintenance_request, name='maintenance_request'),
    path('confirm_booking', views.confirm_booking, name='confirm_booking'),
    path('deny_booking', views.deny_booking, name='deny_booking'),
]
