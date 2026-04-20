from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json
import re
from .models import SchoolUser

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@csrf_exempt
def meta(request):
    """Public metadata endpoint - no authentication required"""
    return JsonResponse({
        'message': 'EduPath API is running!',
        'status': 'ok',
        'version': '1.0',
        'regions': ['West Nile', 'Acholi', 'Lango', 'Kampala', 'Central', 'Eastern', 'Western'],
        'school_types': ['government', 'private', 'catholic', 'protestant', 'islamic', 'international']
    })

@csrf_exempt
def register(request):
    """Register a new school account"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['email', 'school_name', 'password', 'school_type', 'region']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Validate email
        try:
            validate_email(data['email'])
        except ValidationError:
            return JsonResponse({'error': 'Invalid email format'}, status=400)
        
        # Check if email already exists
        if SchoolUser.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)
        
        # Validate password
        is_valid, msg = validate_password(data['password'])
        if not is_valid:
            return JsonResponse({'error': msg}, status=400)
        
        # Create user
        user = SchoolUser.objects.create_user(
            email=data['email'],
            school_name=data['school_name'],
            password=data['password']
        )
        
        # Update additional fields
        user.school_type = data.get('school_type', 'government')
        user.region = data.get('region', 'Kampala')
        user.district = data.get('district', '')
        user.phone = data.get('phone', '')
        user.save()
        
        return JsonResponse({
            'message': 'School account created successfully. Awaiting admin verification.',
            'email': user.email,
            'school_name': user.school_name
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def login_view(request):
    """Authenticate school login"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password required'}, status=400)
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        if not user.is_active:
            return JsonResponse({'error': 'Account is deactivated'}, status=403)
        
        if not user.is_verified:
            return JsonResponse({
                'error': 'Account pending verification',
                'message': 'Please wait for admin approval'
            }, status=403)
        
        # Login user
        login(request, user)
        
        # Return user data (without sensitive info)
        return JsonResponse({
            'message': 'Login successful',
            'user': {
                'id': str(user.id),
                'email': user.email,
                'school_name': user.school_name,
                'school_type': user.school_type,
                'region': user.region,
                'district': user.district,
                'phone': user.phone,
                'is_verified': user.is_verified
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def profile(request):
    """Get or update school profile"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': str(request.user.id),
            'email': request.user.email,
            'school_name': request.user.school_name,
            'school_type': request.user.school_type,
            'region': request.user.region,
            'district': request.user.district,
            'phone': request.user.phone,
            'is_verified': request.user.is_verified,
            'created_at': request.user.created_at.isoformat() if request.user.created_at else None
        })
    
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            
            # Update allowed fields only
            allowed_fields = ['school_name', 'school_type', 'region', 'district', 'phone']
            for field in allowed_fields:
                if field in data:
                    setattr(request.user, field, data[field])
            
            request.user.save()
            return JsonResponse({'message': 'Profile updated successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def change_password(request):
    """Change user password"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return JsonResponse({'error': 'Both old and new password required'}, status=400)
        
        # Verify old password
        if not request.user.check_password(old_password):
            return JsonResponse({'error': 'Current password is incorrect'}, status=400)
        
        # Validate new password
        is_valid, msg = validate_password(new_password)
        if not is_valid:
            return JsonResponse({'error': msg}, status=400)
        
        # Set new password
        request.user.set_password(new_password)
        request.user.save()
        
        return JsonResponse({'message': 'Password changed successfully'})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
def logout_view(request):
    """Logout user"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})