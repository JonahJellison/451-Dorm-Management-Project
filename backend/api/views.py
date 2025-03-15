import json
import hashlib
import os

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import UserAuth

@csrf_exempt
@require_POST
def register_user(request):
    try:
        data = json.load(request.body)
        user_id = data.get('id')
        password = data.get('password')
        if not user_id or not password:
            return HttpResponseBadRequest('ID or Password missing!')
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Something went wrong with the JSON.")
    
    salt = "Salt100"   
    salt_proccessed = salt.encode('utf-8').ljust(16,b'\0')
    
    salted_password = salt + password.encode('utf-8')

    hashed_password = hashlib.sha256(salted_password).hex.digest()

    try:
        user = UserAuth.objects.create(
            user_id=user_id,
            salt=salt.hex(),           # Storing the hex representation of the salt
            hashed_password=hashed_password
        )
    except Exception as e:
        return HttpResponseBadRequest(f"Could not create user: {e}")

    return JsonResponse({'status': 'success', 'message': 'User registered successfully.'})
