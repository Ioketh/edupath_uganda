from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from schools.models import PartnerSchool
from students.models import Student
from accounts.models import SchoolUser
from advertising.models import AdInquiry
import json
import re

def index(request):
    """Serve the main frontend application"""
    return render(request, 'index.html')

def test_page(request):
    """Test page for API debugging"""
    return render(request, 'test.html')

# API Endpoints for Frontend
@csrf_exempt
def api_register(request):
    """School registration API endpoint"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required = ['email', 'school_name', 'password', 'school_type', 'region']
        for field in required:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Check if email exists
        if SchoolUser.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)
        
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
            'message': 'Registration successful. Awaiting admin verification.',
            'email': user.email,
            'school_name': user.school_name
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_login(request):
    """School login API endpoint"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        user = authenticate(request, username=email, password=password)
        
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        if not user.is_verified:
            return JsonResponse({
                'error': 'Account pending verification',
                'message': 'Please wait for admin approval'
            }, status=403)
        
        login(request, user)
        
        return JsonResponse({
            'access': 'demo_token',  # In production, use JWT
            'refresh': 'demo_refresh',
            'school': {
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
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def api_schools(request):
    """Get all partner schools"""
    schools = PartnerSchool.objects.filter(is_partner=True, is_active=True)
    
    # Apply filters
    region = request.GET.get('region')
    school_type = request.GET.get('school_type')
    boarding = request.GET.get('boarding')
    search = request.GET.get('search')
    
    if region:
        schools = schools.filter(region=region)
    if school_type:
        schools = schools.filter(school_type=school_type)
    if boarding:
        schools = schools.filter(boarding=boarding)
    if search:
        schools = schools.filter(name__icontains=search)
    
    data = []
    for school in schools:
        data.append({
            'id': str(school.id),
            'name': school.name,
            'school_type': school.school_type,
            'region': school.region,
            'district': school.district,
            'address': school.address,
            'phone': school.phone,
            'email': school.email,
            'website': school.website,
            'combinations_offered': school.combinations_offered,
            'description': school.description,
            'boarding': school.boarding,
            'is_featured': school.is_featured,
            'logo_url': school.logo.url if school.logo else None,
            'image_url': school.image.url if school.image else None
        })
    
    return JsonResponse({
        'count': len(data),
        'results': data
    })

def api_school_detail(request, pk):
    """Get single school details"""
    try:
        school = PartnerSchool.objects.get(pk=pk, is_partner=True, is_active=True)
        return JsonResponse({
            'id': str(school.id),
            'name': school.name,
            'school_type': school.school_type,
            'motto': school.motto,
            'region': school.region,
            'district': school.district,
            'address': school.address,
            'phone': school.phone,
            'email': school.email,
            'website': school.website,
            'combinations_offered': school.combinations_offered,
            'a_level_students': school.a_level_students,
            'year_founded': school.year_founded,
            'facilities': school.facilities,
            'boarding': school.boarding,
            'description': school.description,
            'is_featured': school.is_featured,
            'logo_url': school.logo.url if school.logo else None,
            'image_url': school.image.url if school.image else None
        })
    except PartnerSchool.DoesNotExist:
        return JsonResponse({'error': 'School not found'}, status=404)

@csrf_exempt
def api_ad_inquiry(request):
    """Submit advertising inquiry"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        inquiry = AdInquiry.objects.create(
            school_name=data.get('school_name'),
            contact_name=data.get('contact_name'),
            phone=data.get('phone'),
            email=data.get('email', ''),
            district=data.get('district', ''),
            combinations=data.get('combinations', ''),
            tier=data.get('tier', 'basic'),
            message=data.get('message', '')
        )
        
        return JsonResponse({
            'message': 'Inquiry received! We will contact you within 24 hours.',
            'inquiry_id': str(inquiry.id)
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_combination_recommend(request):
    """Get combination recommendations based on grades"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        grades = data.get('grades', {})
        
        # Grade points mapping
        grade_points = {'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1}
        
        # Complete combinations list from your frontend
        combinations = [
            {'code': 'PCB', 'subjects': ['Physics', 'Chemistry', 'Biology'], 'name': 'Physics, Chemistry, Biology', 'type': 'Science', 'sub_req': 'Sub-Math'},
            {'code': 'PCM', 'subjects': ['Physics', 'Chemistry', 'Mathematics'], 'name': 'Physics, Chemistry, Mathematics', 'type': 'Science', 'sub_req': 'ICT'},
            {'code': 'BCM', 'subjects': ['Biology', 'Chemistry', 'Mathematics'], 'name': 'Biology, Chemistry, Mathematics', 'type': 'Science', 'sub_req': 'ICT'},
            {'code': 'PEM', 'subjects': ['Physics', 'Economics', 'Mathematics'], 'name': 'Physics, Economics, Mathematics', 'type': 'Science', 'sub_req': 'ICT'},
            {'code': 'HEG', 'subjects': ['History', 'Economics', 'Geography'], 'name': 'History, Economics, Geography', 'type': 'Arts', 'sub_req': 'Sub-Math'},
            {'code': 'HEL', 'subjects': ['History', 'Economics', 'Literature'], 'name': 'History, Economics, Literature', 'type': 'Arts', 'sub_req': 'Sub-Math'},
            {'code': 'MEG', 'subjects': ['Mathematics', 'Economics', 'Geography'], 'name': 'Mathematics, Economics, Geography', 'type': 'Arts', 'sub_req': 'Sub-Math'},
            {'code': 'MEE', 'subjects': ['Mathematics', 'Economics', 'Entrepreneurship'], 'name': 'Mathematics, Economics, Entrepreneurship', 'type': 'Arts', 'sub_req': 'ICT'},
            {'code': 'BCA', 'subjects': ['Biology', 'Chemistry', 'Agriculture'], 'name': 'Biology, Chemistry, Agriculture', 'type': 'Science', 'sub_req': 'Sub-Math'},
            {'code': 'BAG', 'subjects': ['Biology', 'Agriculture', 'Geography'], 'name': 'Biology, Agriculture, Geography', 'type': 'Science', 'sub_req': 'Sub-Math'},
        ]
        
        recommendations = []
        for combo in combinations:
            total = 0
            max_total = 0
            missing = []
            weak = []
            
            for subject in combo['subjects']:
                grade = grades.get(subject)
                if grade:
                    points = grade_points.get(grade, 0)
                    total += points
                    max_total += 6
                    if points < 4:  # C or below is weak
                        weak.append(subject)
                else:
                    missing.append(subject)
            
            percentage = (total / max_total * 100) if max_total > 0 else 0
            
            recommendations.append({
                'code': combo['code'],
                'name': combo['name'],
                'type': combo['type'],
                'sub_req': combo['sub_req'],
                'percentage': round(percentage, 1),
                'weak_subjects': weak,
                'missing_subjects': missing
            })
        
        # Sort by percentage
        recommendations.sort(key=lambda x: x['percentage'], reverse=True)
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations[:5]  # Top 5
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def api_meta(request):
    """Get metadata for frontend (regions, school types, etc.)"""
    return JsonResponse({
        'message': 'EduPath API is running!',
        'status': 'ok',
        'version': '1.0',
        'regions': ['West Nile', 'Acholi', 'Lango', 'Kampala', 'Central', 'Eastern', 'Western'],
        'school_types': ['government', 'private', 'catholic', 'protestant', 'islamic', 'international']
    })

def api_career_check(request):
    """Check career compatibility based on grades"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        career = data.get('career')
        grades = data.get('grades', {})
        
        # Career to combinations mapping (from your frontend)
        career_combos = {
            'Medicine / Surgery': ['PCB', 'BCA', 'BCM'],
            'Engineering (Civil/Electrical/Mechanical)': ['PCM', 'PEM', 'PMTD'],
            'Computer Science / Software Engineering': ['PCM', 'PEM', 'BCM', 'MEE'],
            'Pharmacy': ['PCB', 'BCM', 'BCA'],
            'Nursing / Midwifery': ['PCB', 'BCFN', 'BCA'],
            'Law (LLB)': ['HEL', 'HEG', 'HED', 'HLG'],
            'Business / Commerce / Accounting': ['MEG', 'MEE', 'HEG', 'HEEnt'],
        }
        
        # Grade points
        grade_points = {'A': 6, 'B': 5, 'C': 4, 'D': 3, 'E': 2, 'F': 1}
        
        # Get recommended combos for career
        recommended = career_combos.get(career, [])
        
        # Score each recommended combo
        results = []
        for combo_code in recommended:
            # Find combo details (simplified)
            combo_name = combo_code
            if combo_code == 'PCB':
                subjects = ['Physics', 'Chemistry', 'Biology']
            elif combo_code == 'PCM':
                subjects = ['Physics', 'Chemistry', 'Mathematics']
            elif combo_code == 'BCM':
                subjects = ['Biology', 'Chemistry', 'Mathematics']
            else:
                subjects = []
            
            total = 0
            max_total = len(subjects) * 6
            weak = []
            
            for subject in subjects:
                grade = grades.get(subject)
                if grade:
                    points = grade_points.get(grade, 0)
                    total += points
                    if points < 4:
                        weak.append(subject)
            
            percentage = (total / max_total * 100) if max_total > 0 else 0
            
            results.append({
                'code': combo_code,
                'percentage': percentage,
                'weak': weak
            })
        
        # Determine status
        best_percentage = max([r['percentage'] for r in results]) if results else 0
        if best_percentage >= 70:
            status = 'YES'
            message = f'You qualify for {career} with your current grades!'
        elif best_percentage >= 45:
            status = 'GUIDANCE'
            message = f'You can pursue {career}, but need to strengthen in some subjects.'
        else:
            status = 'NO'
            message = f'Your current grades may not be sufficient for {career}.'
        
        return JsonResponse({
            'status': status,
            'score': best_percentage,
            'message': message,
            'recommendations': results
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)