from django.urls import path
from . import views

urlpatterns = [
    path('meta/', views.meta, name='meta'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]