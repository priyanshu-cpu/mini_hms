from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('book/', views.book_appointment, name='book'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
]
