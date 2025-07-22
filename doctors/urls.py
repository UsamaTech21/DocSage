from django.urls import path
from . import views

urlpatterns = [
    path('', views.find_doctor, name='find_doctor'),
    path('<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]
