from django.urls import path
from . import views

urlpatterns = [
    path('', views.school_list, name='school-list'),
    path('<uuid:pk>/', views.school_detail, name='school-detail'),
    path('featured/', views.featured_schools, name='school-featured'),
    path('my/', views.my_school, name='school-my'),
    path('my/create/', views.create_school, name='school-create'),
    path('my/update/', views.update_school, name='school-update'),
    path('my/upload-logo/', views.upload_logo, name='upload-logo'),
    path('my/upload-image/', views.upload_image, name='upload-image'),
]