from django.db import models

class UserAuth(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default='DefaultUsername')
    salt = models.CharField(max_length=32) 
    hashed_password = models.CharField(max_length=64) 
    email = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id
    

class Student(models.Model):
    student_id = models.IntegerField(unique=True, primary_key=True)
    user = models.OneToOneField(UserAuth, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=255, default='DefaultUsername')
    email = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_id)

'''
Used to identify the booking status of a student for the admin page
'''
class studentBooking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lease_length = models.IntegerField()
    dorm_name = models.CharField(max_length=255)
    room_number = models.CharField(max_length=50)
    confirmed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.booking_id)
    
class Dorm(models.Model):
    dorm_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    dorm = models.ForeignKey(Dorm, related_name='rooms', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    capacity = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    has_AC = models.BooleanField(default=False)
    has_private_bath = models.BooleanField(default=False)
    cost_per_month = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    current_occupants = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.dorm.name} - Room {self.room_number}"