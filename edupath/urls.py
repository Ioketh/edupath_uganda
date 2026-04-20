from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Frontend pages
    path('', views.index, name='index'),
    path('test/', views.test_page, name='test'),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/meta/', views.api_meta, name='api-meta'),
    path('api/auth/register/', views.api_register, name='api-register'),
    path('api/auth/login/', views.api_login, name='api-login'),
    path('api/schools/', views.api_schools, name='api-schools'),
    path('api/schools/<uuid:pk>/', views.api_school_detail, name='api-school-detail'),
    
    # ✅ ADD THIS LINE – include students app URLs
    path('api/students/', include('students.urls')),          # <-- ADD THIS
    
    path('api/advertising/inquire/', views.api_ad_inquiry, name='api-ad-inquiry'),
    path('api/recommend/', views.api_combination_recommend, name='api-recommend'),
    path('api/career/check/', views.api_career_check, name='api-career-check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)