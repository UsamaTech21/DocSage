
from django.urls import path
from . import views

urlpatterns = [
    path('', views.symptom_checker, name='symptom_checker'),
    path('results/', views.symptom_checker_results, name='symptom_checker_results'),
    path('generate-report/<int:predicted_class>/', views.generate_pdf_report, name='generate_pdf_report'),
]
