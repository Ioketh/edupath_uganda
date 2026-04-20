from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import AdInquiry


@admin.register(AdInquiry)
class AdInquiryAdmin(admin.ModelAdmin):
    """Admin interface for advertising inquiries"""
    
    list_display = [
        'school_name',
        'tier_badge',
        'contact_name',
        'phone',
        'district',
        'is_processed',        # Added for list_editable
        'created_at_display',
    ]
    
    list_filter = [
        'tier',
        'is_processed',
        'created_at',
        'district'
    ]
    
    search_fields = [
        'school_name',
        'contact_name',
        'phone',
        'email',
        'district'
    ]
    
    list_editable = ['is_processed']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('School Information', {
            'fields': (
                'school_name',
                'district',
                'combinations',
                'tier',
            ),
            'classes': ('wide',)
        }),
        ('Contact Details', {
            'fields': (
                'contact_name',
                'phone',
                'email',
            ),
            'classes': ('wide',)
        }),
        ('Inquiry Details', {
            'fields': (
                'message',
                'is_processed',
            ),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def tier_badge(self, obj):
        """Display tier with badge styling"""
        badges = {
            'premium': ('⭐ Premium', '#FFD700', '#000'),
            'standard': ('📌 Standard', '#4CAF50', '#fff'),
            'basic': ('📋 Basic', '#9E9E9E', '#fff')
        }
        tier = obj.tier
        if tier in badges:
            label, bg_color, text_color = badges[tier]
            return format_html(
                '<span style="background:{}; color:{}; padding:4px 8px; border-radius:12px; font-weight:bold;">{}</span>',
                bg_color,
                text_color,
                label
            )
        return obj.get_tier_display()
    tier_badge.short_description = 'Package'
    
    def created_at_display(self, obj):
        """Format creation date"""
        return obj.created_at.strftime('%d %b %Y, %H:%M')
    created_at_display.short_description = 'Date'
    
    actions = ['mark_processed', 'create_school_from_inquiry']
    
    def mark_processed(self, request, queryset):
        """Mark inquiries as processed"""
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'✅ {updated} inquiry(s) marked as processed.')
    mark_processed.short_description = '✅ Mark as Processed'
    
    def create_school_from_inquiry(self, request, queryset):
        """Create partner school from inquiry"""
        from schools.models import PartnerSchool
        from accounts.models import SchoolUser
        
        created_count = 0
        for inquiry in queryset:
            if not PartnerSchool.objects.filter(name=inquiry.school_name).exists():
                # Create admin user
                email = inquiry.email or f"{inquiry.school_name.lower().replace(' ', '.')}@school.ug"
                admin_user, _ = SchoolUser.objects.get_or_create(
                    email=email,
                    defaults={
                        'school_name': inquiry.school_name,
                        'phone': inquiry.phone,
                        'district': inquiry.district,
                        'is_verified': True
                    }
                )
                if _:
                    admin_user.set_password('school123')
                    admin_user.save()
                
                # Create school
                PartnerSchool.objects.create(
                    admin=admin_user,
                    name=inquiry.school_name,
                    district=inquiry.district,
                    phone=inquiry.phone,
                    email=email,
                    combinations_offered=inquiry.combinations,
                    ad_tier=inquiry.tier,
                    description=inquiry.message,
                    is_partner=True,
                    is_active=True
                )
                created_count += 1
                inquiry.is_processed = True
                inquiry.save()
        
        self.message_user(request, f'✅ Created {created_count} school(s) from inquiries.')
    create_school_from_inquiry.short_description = '🏫 Create School from Inquiry'