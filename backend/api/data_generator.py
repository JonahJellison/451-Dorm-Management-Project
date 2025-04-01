'''
File to generate random data to pouplate the database
class UserAuth(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default='DefaultUsername')
    salt = models.CharField(max_length=32) 
    hashed_password = models.CharField(max_length=64) 
    email = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class studentBooking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lease_length = models.IntegerField()

    
class Dorm(models.Model):
    dorm_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

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

'''

import random
import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Import models
from api.models import Dorm, Room

dorm_names = ["Duncan Dunn", "Honors Hall", "Global Scholars", "Northside"]
pricing = {'ac': 50, 'private_bath': 100, 'single': 400, 'double': 300, 'triple': 200, 'quad': 100}

dorm_room_data = []

for name in dorm_names:
    for i in range(1, 101): #create 100 rooms for each dorm
        room_number = i
        capacity = random.randint(1, 4)
        has_ac = random.choice([True, False])
        has_private_bath = random.choice([True, False])

        cost = 0
        if capacity == 1:
            cost += pricing['single']
        elif capacity == 2:
            cost += pricing['double']
        elif capacity == 3:
            cost += pricing['triple']
        elif capacity == 4:
            cost += pricing['quad']
        
        if has_ac:
            cost += pricing['ac']
        if has_private_bath:
            cost += pricing['private_bath']

        cost_per_month = cost

        roomdata = {
            'Name': name,
            'RoomNumber': room_number,
            'Capacity': capacity,
            'HasAC': has_ac,
            'HasBath': has_private_bath,
            'MonthlyCost': cost_per_month
        }

        dorm_room_data.append(roomdata)

def populate_database():
    print("Starting database population...")
    
    # First, create the dorms
    dorm_objects = {}
    for name in dorm_names:
        address = f"{random.randint(100, 999)} University Ave, Campus"
        dorm = Dorm.objects.create(
            name=name,
            address=address
        )
        dorm_objects[name] = dorm
        print(f"Created dorm: {name}")
    
    # Then create all the rooms
    room_count = 0
    for room_data in dorm_room_data:
        dorm = dorm_objects[room_data['Name']]
        room = Room.objects.create(
            dorm=dorm,
            room_number=str(room_data['RoomNumber']),
            capacity=room_data['Capacity'],
            is_available=True,
            has_AC=room_data['HasAC'],
            has_private_bath=room_data['HasBath'],
            cost_per_month=room_data['MonthlyCost']
        )
        room_count += 1
        
        # Print progress every 100 rooms
        if room_count % 100 == 0:
            print(f"Created {room_count} rooms so far")
    
    print(f"Database population complete! Created {len(dorm_objects)} dorms and {room_count} rooms.")

if __name__ == '__main__':
    # Check if data already exists to prevent duplicate entries
    existing_dorms = Dorm.objects.count()
    if existing_dorms > 0:
        overwrite = input(f"Found {existing_dorms} existing dorms. Do you want to proceed anyway? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    populate_database()

