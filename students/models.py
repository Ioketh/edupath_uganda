
from django.db import models
from schools.models import PartnerSchool
import uuid

GRADE_CHOICES = [('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F'),('','Not sat')]

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(PartnerSchool, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=200)
    mathematics = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    physics = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    chemistry = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    biology = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    english = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    geography = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    history = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    economics = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    literature = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True)
    career_interest = models.CharField(max_length=200, blank=True)
    best_combination = models.CharField(max_length=20, blank=True)
    match_percentage = models.PositiveIntegerField(default=0)
    guidance_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.school.name}"