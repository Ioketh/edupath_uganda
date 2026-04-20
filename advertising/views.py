from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AdInquiry

@csrf_exempt
def submit_inquiry(request):
    """Submit advertising inquiry"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['school_name', 'contact_name', 'phone']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Create inquiry
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
            'message': 'Inquiry received successfully! Our team will contact you within 24 hours.',
            'inquiry_id': str(inquiry.id)
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def inquiry_status(request, pk):
    """Check inquiry status"""
    try:
        inquiry = AdInquiry.objects.get(pk=pk)
        return JsonResponse({
            'id': str(inquiry.id),
            'school_name': inquiry.school_name,
            'tier': inquiry.tier,
            'is_processed': inquiry.is_processed,
            'created_at': inquiry.created_at.isoformat() if inquiry.created_at else None
        })
    except AdInquiry.DoesNotExist:
        return JsonResponse({'error': 'Inquiry not found'}, status=404)