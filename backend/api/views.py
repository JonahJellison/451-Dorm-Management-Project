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
            return HttpResponseBadRequest("Missing 'id' or 'password'.")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON.")

    # Retrieve the user from the database
    try:
        user = UserAuth.objects.get(user_id=user_id)
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
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
    pass

@csrf_exempt
def fetch_student_data(request):
    pass

@csrf_exempt
def fetch_dormroom_data(request):
    if request.method == 'GET':
        # Get parameters from the URL query string instead of the body
        dorm_name = request.GET.get('building', 'all')
        capacity = request.GET.get('roomType', 'all')
        price_range = request.GET.get('priceRange', 'all')
        
        print("Request parameters:", {
            'building': dorm_name,
            'roomType': capacity,
            'priceRange': price_range
        })

        # Start with all dorm rooms
        rooms = Room.objects.filter(is_available=True)
        
        # Filter by dorm name if not 'all'
        if dorm_name != 'All':
            rooms = rooms.filter(dorm__name=dorm_name)
        
        # Filter by capacity if not 'all'
        if capacity != 'All':
            rooms = rooms.filter(capacity=capacity)
        
        # Filter by price range if not 'all'
        if price_range != 'All':
            if price_range == 'low':
                rooms = rooms.filter(cost_per_month__gte=100, cost_per_month__lt=200)
            elif price_range == 'medium':
                rooms = rooms.filter(cost_per_month__gte=200, cost_per_month__lt=300)
            elif price_range == 'high':
                rooms = rooms.filter(cost_per_month__gte=300)
        
        # Serialize the filtered rooms
        rooms_data = list(rooms.values())
        print(rooms_data[0])
        return JsonResponse({'rooms': rooms_data})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)



