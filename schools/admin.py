from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import PartnerSchool


@admin.register(PartnerSchool)
class PartnerSchoolAdmin(admin.ModelAdmin):
    """
    Comprehensive admin interface for Partner Schools
    """
    
    # List display - include all fields that will be editable
    list_display = [
        'school_icon',
        'name',
        'district',
        'region',
        'school_type_display',
        'is_partner',      # Added for list_editable
        'is_featured',     # Added for list_editable
        'is_active',       # Added for list_editable
        'ad_tier',         # Added for list_editable
        'student_count',
        'created_at_display',
    ]
    
    # List filter - sidebar filters
    list_filter = [
        'is_partner',
        'is_featured',
        'is_active',
        'ad_tier',
        'school_type',
        'region',
        'boarding',
        'created_at',
    ]
    
    # Search fields
    search_fields = [
        'name',
        'district',
        'address',
        'phone',
        'email',
        'admin__email',
        'admin__school_name'
    ]
    
    # Fields that can be edited directly in the list view
    list_editable = [
        'is_partner',
        'is_featured',
        'is_active',
        'ad_tier'
    ]
    
    # Default ordering
    ordering = ['-is_featured', '-is_partner', 'name']
    
    # Pagination
    list_per_page = 25
    
    # Date hierarchy
    date_hierarchy = 'created_at'
    
    # Fields to display in the detail form
    fieldsets = (
        ('🏫 School Identity', {
            'fields': (
                'admin',
                'name',
                'school_type',
                'motto',
                'logo',
                'image'
            ),
            'classes': ('wide',)
        }),
        ('📍 Location Information', {
            'fields': (
                'region',
                'district',
                'address',
            ),
            'classes': ('wide',)
        }),
        ('📞 Contact Details', {
            'fields': (
                'phone',
                'email',
                'website',
            ),
            'classes': ('wide',)
        }),
        ('📚 Academic Information', {
            'fields': (
                'combinations_offered',
                'a_level_students',
                'o_level_streams',
                'year_founded',
                'facilities',
                'boarding',
                'description',
            ),
            'classes': ('wide',)
        }),
        ('💰 Advertising & Visibility', {
            'fields': (
                'ad_tier',
                'is_partner',
                'is_featured',
                'is_active',
            ),
            'description': 'Control school visibility and advertising status',
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Custom methods for display formatting
    def school_icon(self, obj):
        """Display school icon with logo if available"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="width:32px; height:32px; border-radius:8px; object-fit:cover;" />',
                obj.logo.url
            )
        return format_html('<span style="font-size:20px;">🏫</span>')
    school_icon.short_description = ''
    school_icon.admin_order_field = 'name'
    
    def school_type_display(self, obj):
        """Display school type with styling"""
        colors = {
            'government': '#4CAF50',
            'private': '#2196F3',
            'catholic': '#9C27B0',
            'protestant': '#FF9800',
            'islamic': '#009688',
            'international': '#E91E63'
        }
        color = colors.get(obj.school_type, '#757575')
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:12px;">{}</span>',
            color,
            obj.get_school_type_display()
        )
    school_type_display.short_description = 'Type'
    
    def student_count(self, obj):
        """Display number of students"""
        return obj.students.count()
    student_count.short_description = 'Students'
    
    def created_at_display(self, obj):
        """Format created date"""
        return obj.created_at.strftime('%d %b %Y')
    created_at_display.short_description = 'Created'
    created_at_display.admin_order_field = 'created_at'
    
    # Custom actions for bulk operations
    actions = [
        'make_partner',
        'remove_partner',
        'make_featured',
        'remove_featured',
        'activate_schools',
        'deactivate_schools',
        'set_premium_tier',
        'set_standard_tier',
        'set_free_tier'
    ]
    
    def make_partner(self, request, queryset):
        """Bulk approve schools as partners"""
        updated = queryset.update(is_partner=True)
        self.message_user(request, f'✅ {updated} school(s) approved as partners.')
    make_partner.short_description = '✅ Approve as Partner Schools'
    
    def remove_partner(self, request, queryset):
        """Bulk remove partner status"""
        updated = queryset.update(is_partner=False, is_featured=False)
        self.message_user(request, f'❌ Removed partner status from {updated} school(s).')
    remove_partner.short_description = '❌ Remove Partner Status'
    
    def make_featured(self, request, queryset):
        """Bulk mark as featured"""
        updated = queryset.update(is_featured=True, is_partner=True)
        self.message_user(request, f'⭐ {updated} school(s) marked as featured.')
    make_featured.short_description = '⭐ Mark as Featured'
    
    def remove_featured(self, request, queryset):
        """Bulk remove featured status"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'Removed featured status from {updated} school(s).')
    remove_featured.short_description = 'Remove Featured Status'
    
    def activate_schools(self, request, queryset):
        """Bulk activate schools"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✅ Activated {updated} school(s).')
    activate_schools.short_description = '✅ Activate Schools'
    
    def deactivate_schools(self, request, queryset):
        """Bulk deactivate schools"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'⭕ Deactivated {updated} school(s).')
    deactivate_schools.short_description = '⭕ Deactivate Schools'
    
    def set_premium_tier(self, request, queryset):
        """Set advertising tier to premium"""
        updated = queryset.update(ad_tier='premium', is_partner=True)
        self.message_user(request, f'💰 {updated} school(s) upgraded to Premium tier.')
    set_premium_tier.short_description = '💰 Set Premium Tier'
    
    def set_standard_tier(self, request, queryset):
        """Set advertising tier to standard"""
        updated = queryset.update(ad_tier='standard', is_partner=True)
        self.message_user(request, f'📌 {updated} school(s) set to Standard tier.')
    set_standard_tier.short_description = '📌 Set Standard Tier'
    
    def set_free_tier(self, request, queryset):
        """Set advertising tier to free"""
        updated = queryset.update(ad_tier='free')
        self.message_user(request, f'📋 {updated} school(s) set to Free tier.')
    set_free_tier.short_description = '📋 Set Free Tier'
    
    # Save model to handle related data
    def save_model(self, request, obj, form, change):
        """Custom save behavior"""
        if not obj.admin:
            # If no admin assigned, create one
            from accounts.models import SchoolUser
            admin_user, created = SchoolUser.objects.get_or_create(
                email=f"{obj.name.lower().replace(' ', '.')}@school.ug",
                defaults={
                    'school_name': obj.name,
                    'school_type': obj.school_type,
                    'region': obj.region,
                    'district': obj.district,
                    'phone': obj.phone,
                    'is_verified': True,
                    'is_active': True
                }
            )
            if created:
                admin_user.set_password('school123')
                admin_user.save()
            obj.admin = admin_user
        
        super().save_model(request, obj, form, change)
    
    # Add inline for students
    class StudentInline(admin.TabularInline):
        from students.models import Student
        model = Student
        fields = ['name', 'career_interest', 'best_combination', 'match_percentage']
        readonly_fields = ['best_combination', 'match_percentage']
        extra = 1
        show_change_link = True
    
    inlines = [StudentInline]