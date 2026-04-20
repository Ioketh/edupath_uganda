from django.contrib import admin
from django.utils.html import format_html
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for students"""
    
    list_display = [
        'name',
        'school_link',
        'best_combination',
        'match_percentage',
        'career_interest',
        'created_at'
    ]
    
    list_filter = [
        'school',
        'best_combination',
        'career_interest',
        'created_at'
    ]
    
    search_fields = [
        'name',
        'school__name',
        'career_interest'
    ]
    
    list_per_page = 25
    
    fieldsets = (
        ('Student Information', {
            'fields': ('school', 'name', 'career_interest'),
        }),
        ('O-Level Results', {
            'fields': (
                'mathematics', 'physics', 'chemistry', 'biology',
                'english', 'geography', 'history', 'economics', 'literature'
            ),
        }),
        ('Guidance Results', {
            'fields': ('best_combination', 'match_percentage', 'guidance_notes'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    def school_link(self, obj):
        """Link to the school"""
        if obj.school:
            return format_html(
                '<a href="/admin/schools/partnerschool/{}/change/">{}</a>',
                obj.school.id,
                obj.school.name
            )
        return "-"
    school_link.short_description = 'School'