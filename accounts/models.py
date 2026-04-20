from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid

class SchoolUserManager(BaseUserManager):
    def create_user(self, email, school_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, school_name=school_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, school_name='Admin', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, school_name, password, **extra_fields)

class SchoolUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    school_name = models.CharField(max_length=250)
    school_type = models.CharField(max_length=20, choices=[
        ('government', 'Government'),
        ('private', 'Private'),
        ('catholic', 'Catholic'),
        ('protestant', 'Protestant'),
        ('islamic', 'Islamic'),
        ('international', 'International'),
    ], default='government')
    region = models.CharField(max_length=60, choices=[
        ('West Nile', 'West Nile'),
        ('Acholi', 'Acholi'),
        ('Lango', 'Lango'),
        ('Kampala', 'Kampala'),
        ('Central', 'Central'),
        ('Eastern', 'Eastern'),
        ('Western', 'Western'),
    ], default='Kampala')
    district = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=20, choices=[
        ('school_admin', 'School Administrator'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    ], default='school_admin')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = SchoolUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['school_name']
    
    def __str__(self):
        return f"{self.school_name} ({self.email})"


class ParentProfile(models.Model):
    """Parent profile model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(SchoolUser, on_delete=models.CASCADE, related_name='parent_profile')
    children = models.ManyToManyField('students.Student', related_name='parents', blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    preferred_contact = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
    ], default='email')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'accounts_parent_profile'
    
    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"


class LoginHistory(models.Model):
    """Track user login history"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(SchoolUser, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'accounts_login_history'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.timestamp}"