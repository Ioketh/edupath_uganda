from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student-list'),
    path('create/', views.create_student, name='student-create'),
    path('<uuid:pk>/', views.student_detail, name='student-detail'),
    path('<uuid:pk>/update/', views.update_student, name='student-update'),
    path('<uuid:pk>/delete/', views.delete_student, name='student-delete'),
    path('bulk/', views.bulk_add, name='student-bulk'),
    path('export/excel/', views.export_students_excel, name='export-excel'),
    path('export/pdf/', views.export_students_pdf, name='export-pdf'),
]