from django.db import models

class AdInquiry(models.Model):
    school_name = models.CharField(max_length=250)
    contact_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    district = models.CharField(max_length=100, blank=True)
    combinations = models.CharField(max_length=300, blank=True)
    tier = models.CharField(max_length=10, choices=[
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ], default='basic')
    message = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.school_name} - {self.created_at.date()}"