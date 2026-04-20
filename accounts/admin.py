from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import SchoolUser, ParentProfile, LoginHistory


@admin.register(SchoolUser)
class SchoolUserAdmin(UserAdmin):
    """Admin interface for school users"""
    
    list_display = [
        'email',
        'school_name',
        'region',
        'school_type_display',
        'verification_badge',
        'active_badge',
        'date_joined_display'
    ]
    
    list_filter = [
        'user_type',
        'is_verified',
        'is_active',
        'school_type',
        'region',
        'created_at'
    ]
    
    search_fields = [
        'email',
        'school_name',
        'phone',
        'district'
    ]
    
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Login Information', {
            'fields': (
                'email',
                'password',
            ),
            'classes': ('wide',)
        }),
        ('School Information', {
            'fields': (
                'school_name',
                'school_type',
                'region',
                'district',
                'phone',
            ),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': (
                'is_verified',
                'is_active',
                'is_staff',
                'is_superuser',
                'user_type',
            ),
            'classes': ('wide',)
        }),
        ('Permissions', {
            'fields': (
                'groups',
                'user_permissions',
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': (
                'last_login',
                'created_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'school_name',
                'password1',
                'password2',
            ),
        }),
    )
    
    readonly_fields = ['last_login', 'created_at']
    
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
    
    def verification_badge(self, obj):
        """Display verification status"""
        if obj.is_verified:
            return format_html('<span style="color:#4CAF50;">✅ Verified</span>')
        return format_html('<span style="color:#FF9800;">⏳ Pending</span>')
    verification_badge.short_description = 'Status'
    
    def active_badge(self, obj):
        """Display active status"""
        if obj.is_active:
            return format_html('<span style="color:#4CAF50;">● Active</span>')
        return format_html('<span style="color:#F44336;">○ Inactive</span>')
    active_badge.short_description = 'Active'
    
    def date_joined_display(self, obj):
        """Format date joined"""
        return obj.created_at.strftime('%d %b %Y')
    date_joined_display.short_description = 'Joined'
    
    actions = ['verify_users', 'activate_users', 'deactivate_users']
    
    def verify_users(self, request, queryset):
        """Bulk verify school users"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'✅ Verified {updated} school account(s).')
    verify_users.short_description = '✅ Verify Selected Accounts'
    
    def activate_users(self, request, queryset):
        """Bulk activate school users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✅ Activated {updated} school account(s).')
    activate_users.short_description = '✅ Activate Selected Accounts'
    
    def deactivate_users(self, request, queryset):
        """Bulk deactivate school users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'⭕ Deactivated {updated} school account(s).')
    deactivate_users.short_description = '⭕ Deactivate Selected Accounts'


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    """Admin interface for parent profiles"""
    
    list_display = [
        'user',
        'children_count',
        'occupation',
        'preferred_contact_display'
    ]
    
    search_fields = ['user__email', 'user__school_name']
    
    def children_count(self, obj):
        return obj.children.count()
    children_count.short_description = 'Children'
    
    def preferred_contact_display(self, obj):
        return obj.get_preferred_contact_display()
    preferred_contact_display.short_description = 'Contact'


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """Admin interface for login history"""
    
    list_display = [
        'user',
        'ip_address',
        'timestamp_display',
        'success_badge'
    ]
    
    list_filter = ['success', 'timestamp']
    search_fields = ['user__email', 'ip_address']
    
    def timestamp_display(self, obj):
        return obj.timestamp.strftime('%d %b %Y %H:%M')
    timestamp_display.short_description = 'Time'
    timestamp_display.admin_order_field = 'timestamp'
    
    def success_badge(self, obj):
        if obj.success:
            return format_html('<span style="color:#4CAF50;">✓ Success</span>')
        return format_html('<span style="color:#F44336;">✗ Failed</span>')
    success_badge.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False