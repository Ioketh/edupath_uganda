"""
Admin dashboard widgets for school management
"""
from django.contrib.admin import AdminSite
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import PartnerSchool
from students.models import Student
from advertising.models import AdInquiry


class EduPathAdminSite(AdminSite):
    """Custom admin site with dashboard widgets"""
    site_header = 'EduPath Uganda Administration'
    site_title = 'EduPath Uganda'
    index_title = 'School Management Dashboard'
    
    def get_app_list(self, request):
        """Customize app list with statistics"""
        app_list = super().get_app_list(request)
        
        # Add statistics to the dashboard
        stats = {
            'total_schools': PartnerSchool.objects.count(),
            'partner_schools': PartnerSchool.objects.filter(is_partner=True).count(),
            'featured_schools': PartnerSchool.objects.filter(is_featured=True).count(),
            'total_students': Student.objects.count(),
            'pending_inquiries': AdInquiry.objects.filter(is_processed=False).count(),
            'premium_schools': PartnerSchool.objects.filter(ad_tier='premium').count(),
        }
        
        # Add stats to request for custom template
        request.admin_stats = stats
        
        return app_list


# Customize the default admin site
admin_site = EduPathAdminSite(name='edupath_admin')