from django.contrib import admin
from .models import UserAuth, Student, Dorm, Room, studentBooking

admin.site.register(UserAuth)
admin.site.register(Student)    
admin.site.register(Dorm)
admin.site.register(Room)
admin.site.register(studentBooking)
