from django.shortcuts import render, get_object_or_404
from .models import Doctor

def find_doctor(request):
    query = request.GET.get('query', '')
    specialization = request.GET.get('specialization', '')
    location = request.GET.get('location', '')

    doctors = Doctor.objects.all()

    if query:
        doctors = doctors.filter(name__icontains=query)

    if specialization:
        doctors = doctors.filter(expertise__icontains=specialization)

    if location:
        doctors = doctors.filter(location__icontains=location)

    return render(request, 'doctors/find_doctor.html', {'doctors': doctors})


def doctor_detail(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})


def doctor_dashboard(request):
    return render(request, 'doctors/doctor_dashboard.html')


def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})
