from schools.models import PartnerSchool
from students.models import Student
from advertising.models import AdInquiry

def admin_stats(request):
    """Provide statistics for the custom admin dashboard (safe for login page)"""
    # Only add stats for authenticated admin users (not on login page)
    if request.user.is_authenticated and request.path.startswith('/admin/'):
        try:
            # Calculate statistics
            total_schools = PartnerSchool.objects.count()
            partner_schools = PartnerSchool.objects.filter(is_partner=True).count()
            featured_schools = PartnerSchool.objects.filter(is_featured=True).count()
            premium_schools = PartnerSchool.objects.filter(ad_tier='premium').count()
            total_students = Student.objects.count()
            pending_inquiries = AdInquiry.objects.filter(is_processed=False).count()
            
            # Recent schools and inquiries
            recent_schools = PartnerSchool.objects.order_by('-created_at')[:10]
            recent_inquiries = AdInquiry.objects.order_by('-created_at')[:10]
            
            return {
                'admin_stats': {
                    'total_schools': total_schools,
                    'partner_schools': partner_schools,
                    'featured_schools': featured_schools,
                    'premium_schools': premium_schools,
                    'total_students': total_students,
                    'pending_inquiries': pending_inquiries,
                },
                'recent_schools': recent_schools,
                'recent_inquiries': recent_inquiries,
            }
        except Exception:
            # If any database error occurs (e.g., tables not migrated), return empty
            return {}
    return {}