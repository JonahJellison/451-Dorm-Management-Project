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

@csrf_exempt
def fetch_student_data(request):
    if request.method == 'GET':
        student_id = request.GET.get('studentId')
        if not student_id:
            return HttpResponseBadRequest("Missing studentId parameter.")
        try:
            user = UserAuth.objects.get(user_id=student_id)
            data = {
                'student_id': user.user_id,
                'name': user.name,
                'email': user.email,
            }
            return JsonResponse(data)
        except UserAuth.DoesNotExist:
            return HttpResponseBadRequest("Student not found.")
    else:
        return HttpResponseBadRequest("Invalid request method.")

@csrf_exempt
def student_info_view(request):
    if request.method == 'GET':
        # Retrieve the studentId from the query string
        student_id = request.GET.get('studentId')
        if not student_id:
            return HttpResponseBadRequest("Missing studentId parameter.")
        try:
            user = UserAuth.objects.get(user_id=student_id)
        except UserAuth.DoesNotExist:
            return HttpResponseBadRequest("Student not found.")
        
        # Try to get the associated StudentInfo record, if it exists
        try:
            info = StudentInfo.objects.get(user=user)
        except StudentInfo.DoesNotExist:
            info = None

        response_data = {
            'student_id': user.user_id,
            'phone_number': info.phone_number if info else None,
            'home_address': info.home_address if info else None,
            'emergency_contact': info.emergency_contact if info else None,
        }
        return JsonResponse(response_data)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data.")

        student_id = data.get('studentId')
        if not student_id:
            return HttpResponseBadRequest("Missing studentId in JSON data.")

        try:
            user = UserAuth.objects.get(user_id=student_id)
        except UserAuth.DoesNotExist:
            return HttpResponseBadRequest("Student not found.")

        # Get the values to update/create
        phone_number = data.get('phone_number')
        home_address = data.get('home_address')
        emergency_contact = data.get('emergency_contact')

        # Create or update the StudentInfo record linked to the user
        info, created = StudentInfo.objects.update_or_create(
            user=user,
            defaults={
                'phone_number': phone_number,
                'home_address': home_address,
                'emergency_contact': emergency_contact,
            }
        )

        response_data = {
            'status': 'success',
            'message': 'Student info updated successfully.' if not created else 'Student info created successfully.',
            'student_id': user.user_id,
            'phone_number': info.phone_number,
            'home_address': info.home_address,
            'emergency_contact': info.emergency_contact,
        }
        return JsonResponse(response_data)
    
    else:
        return HttpResponseBadRequest("Invalid request method. Use GET or POST.")

@csrf_exempt
def update_user_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data.")
        
        user_id = data.get('user_id')
        if not user_id:
            return HttpResponseBadRequest("Missing user_id in request.")
        
        try:
            user = UserAuth.objects.get(user_id=user_id)
        except UserAuth.DoesNotExist:
            return HttpResponseBadRequest("User not found.")
        
        # Retrieve new values for name and email from the payload.
        new_name = data.get('name')
        new_email = data.get('email')
        
        # Optional: Validate that new_name and new_email are provided.
        if not new_name or not new_email:
            return HttpResponseBadRequest("Both name and email must be provided.")
        
        user.name = new_name
        user.email = new_email
        
        try:
            user.save()
        except Exception as e:
            return HttpResponseBadRequest(f"Error updating user info: {str(e)}")
        
        response_data = {
            'status': 'success',
            'message': 'User info updated successfully.',
            'user': {
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email
            }
        }
        return JsonResponse(response_data)
    else:
        return HttpResponseBadRequest("Invalid request method. Use POST.")
    

@csrf_exempt
def maintenance_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            student_id = data.get('studentId')
            location = data.get('location')
            issue = data.get('issue')
            submissionDate = data.get('submissionDate')
            priority = data.get('priority')
            
            # Validate required fields
            if not all([student_id, location, issue, submissionDate, priority]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing required fields'
                }, status=400)
                
            # Get the user
            try:
                user = UserAuth.objects.get(user_id=student_id)
            except UserAuth.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Student not found'
                }, status=404)
                
            new_request = MaintenanceRequest(
                student_id = student_id,
                issue = issue,
                location = location,    
                priority = priority,
                date_created = submissionDate
            )
            new_request.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Maintenance request submitted successfully',
                'request_id': new_request.request_id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error processing request: {str(e)}'
            }, status=500)
    
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed. Use POST to create a request or GET to retrieve requests.'
        }, status=405)



@csrf_exempt
def fetch_admin_data(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        # bookings
        bookings_data = []
        for b in studentBooking.objects.all():
            bookings_data.append({
                'id': b.booking_id,
                'student_id': b.student_id.user_id,
                'booking_date': b.booking_date.isoformat(),
                'lease_length': b.lease_length,
                'dorm_name': b.dorm_name,
                'room_number': b.room_number,
                'confirmed': b.confirmed,
            })

        # maintenance
        maintenance_data = []
        for m in MaintenanceRequest.objects.all():
            maintenance_data.append({
                'id': m.request_id,
                'student_id': m.student_id,
                'issue': m.issue,
                'location': m.location,
                'priority': m.priority,
                'date_created': m.date_created,
            })

        # occupied rooms
        occupied_data = []
        for r in Room.objects.filter(is_available=False):
            occupied_data.append({
                'room_id': r.room_id,
                'dorm_name': r.dorm.name,
                'room_number': r.room_number,
                'capacity': r.capacity,
                'current_occupants': r.current_occupants,
            })

        return JsonResponse({
            'bookings': bookings_data,
            'maintenance_requests': maintenance_data,
            'occupied_rooms': occupied_data
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def update_booking(request):
    """
    Payload: { booking_id: number, status: 'Pending'|'Confirmed'|'Denied' }
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        bid = data.get('booking_id')
        status = data.get('status')
        if bid is None or status not in ('Pending','Confirmed','Denied'):
            return JsonResponse({'status':'error','message':'Invalid parameters'}, status=400)

        bk = studentBooking.objects.get(booking_id=bid)

        # tri-state
        if status == 'Confirmed':
            bk.confirmed = True
            sendEmail(bk.student_id.email, "Your booking has been confirmed.")
        elif status == 'Denied':
            bk.confirmed = False
            sendEmail(bk.student_id.email, "Your booking has been denied.")
        else:
            bk.confirmed = None

        bk.save()
        return JsonResponse({'status':'success','message':'Booking updated.'})

    except studentBooking.DoesNotExist:
        return JsonResponse({'status':'error','message':'Booking not found'}, status=404)

    except Exception as e:
        # <— print the full traceback or repr so you see exactly what went wrong
        import traceback; traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': f'Unexpected error: {e!r}'
        }, status=500)


@csrf_exempt
def confirm_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            # get booking ID for confirmation
            booking_id = data.get('booking_id')

            #get student id for email info
            student_id = data.get('student_id')
            student = Student.objects.get(student_id=student_id)
            student_email = student.email

            if not booking_id:
                return JsonResponse({'status': 'error', 'message': 'Missing booking ID'}, status=400)
                
            try:
                booking = studentBooking.objects.get(booking_id=booking_id)
                
                # Update room availability
                try:
                    room = Room.objects.get(dorm__name=booking.dorm_name, room_number=booking.room_number)
                    room.current_occupants += 1
                    if room.current_occupants < room.capacity:
                        room.is_available = True
                    else:
                        room.is_available = False
                    room.save()
                except Room.DoesNotExist:
                    # Continue with deletion even if room not found
                    pass
                
                # Delete the booking
                booking.delete()
                sendEmail(student_email, "Your booking has been confirmed. Congraduations")
                return JsonResponse({
                    'status': 'success',
                    'message': 'Booking denied and deleted successfully'
                })
                
            except studentBooking.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Booking not found'
                }, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error denying booking: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed. Use POST method.'
        }, status=405)


@csrf_exempt
def deny_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            # get booking info
            booking_id = data.get('booking_id')

            # get student email info
            student_id = data.get('student_id')
            student = Student.objects.get(student_id=student_id)
            student_email = student.email

            if not booking_id:
                return JsonResponse({'status': 'error', 'message': 'Missing booking ID'}, status=400)
                
            try:
                booking = studentBooking.objects.get(booking_id=booking_id)
                
                # Update room availability
                try:
                    room = Room.objects.get(dorm__name=booking.dorm_name, room_number=booking.room_number)
                    room.current_occupants -= 1
                    if room.current_occupants < 0:
                        room.current_occupants = 0
                    if room.current_occupants < room.capacity:
                        room.is_available = True
                    room.save()
                    sendEmail(student_email, "Unfortunately, your booking has been denied. Contact your housing coordinator for more information")
                except Room.DoesNotExist:
                    # Continue with deletion even if room not found
                    pass
                
                # Delete the booking
                booking.delete()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Booking denied and deleted successfully'
                })
                
            except studentBooking.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Booking not found'
                }, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error denying booking: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed. Use POST method.'
        }, status=405)


@csrf_exempt
def verify_admin(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(f"DEBug: {data}")
        userid = data.get('id')
        user = UserAuth.objects.get(user_id=userid)
        if user.is_admin:
            return JsonResponse({'status': True, 'message': 'User is an admin.'})
        else:
            return JsonResponse({'status': False, 'message': 'User is not an admin.'})


@csrf_exempt
def add_admin(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('id')
            if not user_id:
                return JsonResponse({'status': 'error', 'message': 'Missing user_id in request.'}, status=400)
            
            # Retrieve the user from the database
            try:
                user = UserAuth.objects.get(user_id=user_id)
                user.is_admin = True  # Set the is_admin field to True
                user.save()  # Save the changes to the database
                return JsonResponse({'status': 'success', 'message': 'User added as admin successfully.'})
            except UserAuth.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
        

@csrf_exempt
def delete_maintenance_request(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body.decode('utf-8'))
            request_id = data.get('request_id')
            student_id = data.get('student_id')
            student = Student.objects.get(student_id=student_id)
            student_email = student.email

            if not request_id:
                return JsonResponse({'status': 'error', 'message': 'Missing booking ID'}, status=400)
                
            try:
                maintenance_request = MaintenanceRequest.objects.get(request_id=request_id)
                
                # Delete the booking
                maintenance_request.delete()
                sendEmail(student_email, "Your maintainence request has been reviewed by an administrator")

                return JsonResponse({
                    'status': 'success',
                    'message': 'Booking deleted successfully'
                })
                
            except MaintenanceRequest.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Booking not found'
                }, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error deleting booking: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed. Use DELETE method.'
        }, status=405)
            

def sendEmail(address, message):
    #TODO: jonah impliment
    pass