from django.db import models
from accounts.models import SchoolUser
import os
import uuid

def school_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'schools/{instance.id}/image{ext}'

def school_logo_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'schools/{instance.id}/logo{ext}'

class PartnerSchool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, related_name='partner_school')
    name = models.CharField(max_length=250)
    school_type = models.CharField(max_length=20, choices=[
        ('government', 'Government'),
        ('private', 'Private'),
        ('catholic', 'Catholic'),
        ('protestant', 'Protestant'),
        ('islamic', 'Islamic'),
    ], default='government')
    motto = models.CharField(max_length=200, blank=True)
    region = models.CharField(max_length=60)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to=school_logo_path, blank=True, null=True)
    image = models.ImageField(upload_to=school_image_path, blank=True, null=True)
    combinations_offered = models.TextField(blank=True)
    a_level_students = models.PositiveIntegerField(default=0)
    o_level_streams = models.PositiveIntegerField(default=1)
    year_founded = models.PositiveIntegerField(null=True, blank=True)
    facilities = models.TextField(blank=True)
    boarding = models.CharField(max_length=10, choices=[
        ('day', 'Day Only'),
        ('boarding', 'Boarding Only'),
        ('both', 'Day & Boarding'),
    ], default='day')
    description = models.TextField(blank=True, max_length=600)
    ad_tier = models.CharField(max_length=10, choices=[
        ('free', 'Free'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ], default='free')
    is_partner = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name