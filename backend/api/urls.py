from django.urls import path, include
from api import views


urlpatterns = [
    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm-email'),
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
    path('update_booking',    views.update_booking,    name='update_booking'),
    path('verify_admin', views.verify_admin, name='verify_admin'),
    path('add_admin', views.add_admin, name='add_admin'),
    path('update_maintenance', views.update_maintenance, name='update_maintenance'),
    path('request-password-reset', views.request_password_reset, name='request-password-reset'),
    path('reset-password', views.reset_password, name='reset-password'),
]

