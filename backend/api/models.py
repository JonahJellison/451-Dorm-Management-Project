from django.db import models

# Create your models here.
class Resident(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class Building(models.Model):
    building_id = models.AutoField(primary_key=True)
    room_count = models.IntegerField()
    num_floors = models.IntegerField()
    max_capacity = models.IntegerField()

class Room(models.Model):
    room_num = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor_num = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    has_ac = models.BooleanField()
    has_wifi = models.BooleanField()
    max_occupants = models.IntegerField()

    class Meta:
        unique_together = (('building', 'room_num'),)

class Lease(models.Model):
    lease_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Resident, on_delete=models.CASCADE)

class ResidentLease(models.Model):
    lease = models.OneToOneField(Lease, on_delete=models.CASCADE, primary_key=True)
    student = models.ForeignKey(Resident, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_num = models.IntegerField()
    date = models.DateField()
    length = models.IntegerField()
    is_full = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (('building', 'room_num'),)