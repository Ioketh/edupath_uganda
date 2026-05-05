from django.core.exceptions import ImproperlyConfigured

def admin_stats(request):
    """Provide statistics and recent items for the admin dashboard."""
    stats = {}
    recent_schools = []
    recent_inquiries = []

    try:
        from schools.models import PartnerSchool
        from advertising.models import AdInquiry
        from students.models import Student

        total_schools = PartnerSchool.objects.count()
        partner_schools = PartnerSchool.objects.filter(is_partner=True).count()
        featured_schools = PartnerSchool.objects.filter(ad_tier='premium').count()
        total_students = Student.objects.count()
        pending_inquiries = AdInquiry.objects.filter(is_processed=False).count()
        premium_schools = PartnerSchool.objects.filter(ad_tier='premium').count()

        recent_schools = PartnerSchool.objects.order_by('-created_at')[:5]
        recent_inquiries = AdInquiry.objects.order_by('-created_at')[:5]

        stats = {
            'total_schools': total_schools,
            'partner_schools': partner_schools,
            'featured_schools': featured_schools,
            'total_students': total_students,
            'pending_inquiries': pending_inquiries,
            'premium_schools': premium_schools,
        }
    except Exception as e:
        # Fail gracefully – admin page will still load with zeros
        stats = {
            'total_schools': 0,
            'partner_schools': 0,
            'featured_schools': 0,
            'total_students': 0,
            'pending_inquiries': 0,
            'premium_schools': 0,
        }

    return {
        'admin_stats': stats,
        'recent_schools': recent_schools,
        'recent_inquiries': recent_inquiries,
    }