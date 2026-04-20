from schools.models import PartnerSchool
from advertising.models import AdInquiry


def admin_stats(request):
    """Add statistics to admin context"""
    if request.path.startswith('/admin/'):
        return {
            'recent_schools': PartnerSchool.objects.order_by('-created_at')[:10],
            'recent_inquiries': AdInquiry.objects.order_by('-created_at')[:10],
            'admin_stats': {
                'total_schools': PartnerSchool.objects.count(),
                'partner_schools': PartnerSchool.objects.filter(is_partner=True).count(),
                'featured_schools': PartnerSchool.objects.filter(is_featured=True).count(),
                'premium_schools': PartnerSchool.objects.filter(ad_tier='premium').count(),
                'pending_inquiries': AdInquiry.objects.filter(is_processed=False).count(),
            }
        }
    return {}