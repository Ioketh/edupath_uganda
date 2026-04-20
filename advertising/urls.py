from django.urls import path
from . import views

urlpatterns = [
    path('inquire/', views.submit_inquiry, name='ad-inquire'),
    path('status/<uuid:pk>/', views.inquiry_status, name='ad-status'),
]