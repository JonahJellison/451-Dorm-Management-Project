import json
import hashlib
import os
from .models import *
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import UserAuth
import requests
import json
from datetime import datetime  # Add this import at the top

@csrf_exempt  # For testing purposes. In production, ensure proper CSRF handling.
@require_POST
def register_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username=data.get('fullname')
        user_id = data.get('studentid')
        password = data.get('password')
        email = data.get('email')
        if not user_id or not password:
            return HttpResponseBadRequest('ID or Password missing!')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Something went wrong with the JSON.")
    
    # Create a static salt "Salt100" and pad it to 16 bytes.
    salt = "Salt100"
    salt_processed = salt.encode('utf-8').ljust(16, b'\0')
    
    # Combine the padded salt with the password.
    salted_password = salt_processed + password.encode('utf-8')
    
    # Correct hash call.
    hashed_password = hashlib.sha256(salted_password).hexdigest()

    print(hashed_password)
    try:
        user = UserAuth.objects.create(
            user_id=user_id,
            name=username,
            salt=salt_processed.hex(),  # Use the processed salt's hex representation
            hashed_password=hashed_password,
            email=email
        )
        # Save the user to the database
        user.save()
        # Return success after saving the user
    except Exception as e:
        return HttpResponseBadRequest(f"Could not create user: {e}")

    return JsonResponse({'status': 'success', 'message': 'User registered successfully.'})
   
@csrf_exempt  # For testing purposes. In production, ensure proper CSRF handling.
@require_POST
def login_user(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('id')
        password = data.get('password')
        if not user_id or not password:
            print("Missing 'id' or 'password'.")
            return HttpResponseBadRequest("Missing 'id' or 'password'.")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON.")

    # Retrieve the user from the database
    try:
        user = UserAuth.objects.get(user_id=user_id)
        print("User found:", user.user_id)
    except UserAuth.DoesNotExist:
        return HttpResponseBadRequest("User does not exist.")

    # Convert the stored hex salt back to bytes
    salt_bytes = bytes.fromhex(user.salt)
    
    # Combine the salt with the provided password (encode the password)
    salted_password = salt_bytes + password.encode('utf-8')
    
    # Hash the combined bytes using SHA256
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    
    # Compare the computed hash with the stored hash
    if hashed_password == user.hashed_password:
        return JsonResponse({'status': 'success', 'message': 'Login successful.'})
    else:
        return HttpResponseBadRequest("Invalid password.")
    

@csrf_exempt
def fetch_admin_data(request):
    if request.method == 'GET':
        print("Fetching admin data...")
    # Fetch all student bookings and return as JSON response
        try:
            bookings = studentBooking.objects.all()
            bookings_data = []
            
            for booking in bookings:
                booking_dict = {
                    'id': booking.booking_id,
                    'student_id': booking.student_id,
                    'lease_length': booking.lease_length,
                    'dorm_name': booking.dorm_name,
                    'room_number': booking.room_number,
                    'confirmed': booking.confirmed
                }
                bookings_data.append(booking_dict)
            
            return JsonResponse({'bookings': bookings_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def fetch_student_data(request):
    pass

@csrf_exempt
def fetch_dormroom_data(request):
    if request.method == 'GET':
        # Get parameters from the URL query string instead of the body
        building_param = request.GET.get('building', 'all')
        room_type_param = request.GET.get('roomType', 'all')
        price_range = request.GET.get('priceRange', 'all')
        
        print("Request parameters:", {
            'building': building_param,
            'roomType': room_type_param,
            'priceRange': price_range
        })

        # Map frontend building codes to dorm names
        building_map = {
            'north': 'Duncan Dunn',
            'south': 'Honors Hall',
            'east': 'Global Scholars',
            'west': 'Northside'
        }
        
        # Map frontend room types to capacity values
        room_type_map = {
            'single': 1,
            'double': 2,
            'triple': 3
        }
        
        # Start with all available dorm rooms
        rooms = Room.objects.filter(is_available=True)
        
        # Filter by dorm name if specified
        if building_param and building_param.lower() != 'all':
            dorm_name = building_map.get(building_param)
            if dorm_name:
                rooms = rooms.filter(dorm__name=dorm_name)
        
        # Filter by room type if specified
        if room_type_param and room_type_param.lower() != 'all':
            capacity = room_type_map.get(room_type_param)
            if capacity:
                rooms = rooms.filter(capacity=capacity)
        
        # Filter by price range if specified
        if price_range and price_range.lower() != 'all':
            if price_range == 'low':
                rooms = rooms.filter(cost_per_month__gte=100, cost_per_month__lt=200)
            elif price_range == 'medium':
                rooms = rooms.filter(cost_per_month__gte=200, cost_per_month__lt=300)
            elif price_range == 'high':
                rooms = rooms.filter(cost_per_month__gte=300)
        
        # Serialize the filtered rooms with dorm name
        rooms_data = []
        for room in rooms:
            room_dict = {
                'room_id': room.room_id,
                'dorm_name': room.dorm.name,
                'room_number': room.room_number,
                'capacity': room.capacity,
                'has_AC': room.has_AC,
                'has_private_bath': room.has_private_bath,
                'cost_per_month': float(room.cost_per_month)
            }
            rooms_data.append(room_dict)
        
        print(f"{len(rooms_data)} rooms found.")
        return JsonResponse({'rooms': rooms_data})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)



@csrf_exempt 
def book_room(request):
    '''
    Expected request data:
    {
        room_id: number;
        request_roommate: boolean;
        roommate_student_id: string | null;
        lease_duration: number;
    }
    '''
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            room_id = data.get('room_id')
            roommate_id = data.get('roommate_student_id', None)
            student_id = data.get('student_id', 1234)
            lease_length = data.get('lease_duration', 6)  # Default to 6 months
            print(f"Data params: {room_id}, {roommate_id}, {student_id}, {lease_length}")
            try:
                # Find the room by its primary key (room_id) to get dorm_name and room_number
                room = Room.objects.get(pk=room_id)
                print(f"Room from db: {room}")
                
                # Check if the room is already fully booked
                if room.current_occupants >= room.capacity:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Room is already fully booked.'
                    }, status=400)
                    
                dorm_name = room.dorm.name
                room_number = room.room_number
                print(f"Room number: {room_number}, Dorm name: {dorm_name}")
                
                # Get the UserAuth object first
                try:
                    user = UserAuth.objects.get(user_id=student_id)
                    
                    newBooking = studentBooking(
                        student_id=user,
                        lease_length=lease_length,
                        dorm_name=dorm_name,
                        room_number=room_number,
                        confirmed=False  
                    )
                    print("New booking created:", newBooking)
                    
                    # Save the booking to the database
                    newBooking.save()
                    print("Booking saved:", newBooking)
                    
                    # Update the room availability only once
                    room.current_occupants += 1
                    if room.current_occupants >= room.capacity:
                        room.is_available = False
                    else:
                        room.is_available = True
                    room.save()
                    print("Room updated:", room)
                    
                    return JsonResponse({
                        'status': 'success', 
                        'message': 'Room booked successfully.',
                        'booking_id': newBooking.booking_id
                    })
                    
                except UserAuth.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Student ID not found.'
                    }, status=404)
                
            except Room.DoesNotExist:
                print("Room not found.")
                return JsonResponse({
                'status': 'error',
                'message': 'Room not found.'
                }, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data.'
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
            'status': 'error',
            'message': f'Error booking room: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method. Use POST.'
    }, status=405)


