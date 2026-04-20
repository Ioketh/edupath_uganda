from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
import json
from .models import PartnerSchool
from accounts.models import SchoolUser

def school_list(request):
    """Public list of approved partner schools with filtering"""
    schools = PartnerSchool.objects.filter(is_partner=True, is_active=True)
    
    # Apply filters
    region = request.GET.get('region')
    school_type = request.GET.get('school_type')
    boarding = request.GET.get('boarding')
    combination = request.GET.get('combination')
    search = request.GET.get('search')
    
    if region:
        schools = schools.filter(region=region)
    if school_type:
        schools = schools.filter(school_type=school_type)
    if boarding:
        schools = schools.filter(boarding=boarding)
    if combination:
        schools = schools.filter(combinations_offered__icontains=combination)
    if search:
        schools = schools.filter(
            Q(name__icontains=search) |
            Q(district__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(schools, 20)
    
    try:
        schools_page = paginator.page(page)
    except:
        schools_page = paginator.page(1)
    
    data = []
    for school in schools_page:
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
            'logo_url': school.logo.url if school.logo else None,
            'image_url': school.image.url if school.image else None,
            'combinations_offered': school.combinations_offered,
            'a_level_students': school.a_level_students,
            'year_founded': school.year_founded,
            'facilities': school.facilities,
            'boarding': school.boarding,
            'description': school.description,
            'ad_tier': school.ad_tier,
            'is_featured': school.is_featured,
            'created_at': school.created_at.isoformat() if school.created_at else None
        })
    
    return JsonResponse({
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': int(page),
        'results': data
    })

def school_detail(request, pk):
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
            'logo_url': school.logo.url if school.logo else None,
            'image_url': school.image.url if school.image else None,
            'combinations_offered': school.combinations_offered,
            'a_level_students': school.a_level_students,
            'o_level_streams': school.o_level_streams,
            'year_founded': school.year_founded,
            'facilities': school.facilities,
            'boarding': school.boarding,
            'description': school.description,
            'ad_tier': school.ad_tier,
            'is_featured': school.is_featured,
            'created_at': school.created_at.isoformat() if school.created_at else None
        })
    except PartnerSchool.DoesNotExist:
        return JsonResponse({'error': 'School not found'}, status=404)

def featured_schools(request):
    """Get featured schools for landing page"""
    schools = PartnerSchool.objects.filter(
        is_partner=True, 
        is_featured=True, 
        is_active=True
    ).order_by('-ad_tier')[:6]
    
    data = []
    for school in schools:
        data.append({
            'id': str(school.id),
            'name': school.name,
            'district': school.district,
            'logo_url': school.logo.url if school.logo else None,
            'ad_tier': school.ad_tier
        })
    
    return JsonResponse({'featured': data})

def schools_by_region(request):
    """Group schools by region"""
    schools = PartnerSchool.objects.filter(is_partner=True, is_active=True)
    regions = {}
    
    for school in schools:
        if school.region not in regions:
            regions[school.region] = []
        regions[school.region].append({
            'id': str(school.id),
            'name': school.name,
            'district': school.district
        })
    
    return JsonResponse(regions)

@csrf_exempt
def my_school(request):
    """Get authenticated school's own profile"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        school = PartnerSchool.objects.get(admin=request.user)
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
            'logo_url': school.logo.url if school.logo else None,
            'image_url': school.image.url if school.image else None,
            'combinations_offered': school.combinations_offered,
            'a_level_students': school.a_level_students,
            'o_level_streams': school.o_level_streams,
            'year_founded': school.year_founded,
            'facilities': school.facilities,
            'boarding': school.boarding,
            'description': school.description,
            'ad_tier': school.ad_tier,
            'is_partner': school.is_partner,
            'is_featured': school.is_featured,
            'is_active': school.is_active,
            'created_at': school.created_at.isoformat() if school.created_at else None,
            'updated_at': school.updated_at.isoformat() if school.updated_at else None
        })
    except PartnerSchool.DoesNotExist:
        return JsonResponse({'error': 'School profile not found'}, status=404)

@csrf_exempt
def create_school(request):
    """Create school profile (authenticated)"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    # Check if profile already exists
    if PartnerSchool.objects.filter(admin=request.user).exists():
        return JsonResponse({'error': 'Profile already exists'}, status=400)
    
    try:
        data = json.loads(request.body)
        
        # Create school profile
        school = PartnerSchool.objects.create(
            admin=request.user,
            name=data.get('name', request.user.school_name),
            school_type=data.get('school_type', request.user.school_type),
            motto=data.get('motto', ''),
            region=data.get('region', request.user.region),
            district=data.get('district', request.user.district),
            address=data.get('address', ''),
            phone=data.get('phone', request.user.phone),
            email=data.get('email', request.user.email),
            website=data.get('website', ''),
            combinations_offered=data.get('combinations_offered', ''),
            a_level_students=data.get('a_level_students', 0),
            o_level_streams=data.get('o_level_streams', 1),
            year_founded=data.get('year_founded', None),
            facilities=data.get('facilities', ''),
            boarding=data.get('boarding', 'day'),
            description=data.get('description', ''),
            ad_tier='free'  # Default free tier
        )
        
        return JsonResponse({
            'message': 'School profile created successfully. Pending admin review.',
            'school_id': str(school.id)
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def update_school(request):
    """Update school profile (authenticated)"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method != 'PATCH':
        return JsonResponse({'error': 'PATCH method required'}, status=405)
    
    try:
        school = PartnerSchool.objects.get(admin=request.user)
        data = json.loads(request.body)
        
        # Update allowed fields
        allowed_fields = ['name', 'school_type', 'motto', 'region', 'district', 
                         'address', 'phone', 'email', 'website', 'combinations_offered',
                         'a_level_students', 'o_level_streams', 'year_founded', 
                         'facilities', 'boarding', 'description']
        
        for field in allowed_fields:
            if field in data:
                setattr(school, field, data[field])
        
        school.save()
        
        return JsonResponse({'message': 'School profile updated successfully'})
        
    except PartnerSchool.DoesNotExist:
        return JsonResponse({'error': 'School profile not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
def upload_logo(request):
    """Upload school logo"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        school = PartnerSchool.objects.get(admin=request.user)
        
        if 'logo' not in request.FILES:
            return JsonResponse({'error': 'No logo file provided'}, status=400)
        
        logo_file = request.FILES['logo']
        
        # Validate file size (max 2MB)
        if logo_file.size > 2 * 1024 * 1024:
            return JsonResponse({'error': 'Logo must be under 2MB'}, status=400)
        
        # Validate file type
        if not logo_file.content_type.startswith('image/'):
            return JsonResponse({'error': 'File must be an image'}, status=400)
        
        # Delete old logo if exists
        if school.logo:
            school.logo.delete(save=False)
        
        school.logo = logo_file
        school.save()
        
        return JsonResponse({
            'message': 'Logo uploaded successfully',
            'logo_url': school.logo.url if school.logo else None
        })
        
    except PartnerSchool.DoesNotExist:
        return JsonResponse({'error': 'School profile not found'}, status=404)

@csrf_exempt
def upload_image(request):
    """Upload school banner image"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        school = PartnerSchool.objects.get(admin=request.user)
        
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)
        
        image_file = request.FILES['image']
        
        # Validate file size (max 5MB)
        if image_file.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'Image must be under 5MB'}, status=400)
        
        # Validate file type
        if not image_file.content_type.startswith('image/'):
            return JsonResponse({'error': 'File must be an image'}, status=400)
        
        # Delete old image if exists
        if school.image:
            school.image.delete(save=False)
        
        school.image = image_file
        school.save()
        
        return JsonResponse({
            'message': 'Image uploaded successfully',
            'image_url': school.image.url if school.image else None
        })
        
    except PartnerSchool.DoesNotExist:
        return JsonResponse({'error': 'School profile not found'}, status=404)