from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.contrib.auth.models import User

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/default.jpg')
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    blood_group = models.CharField(max_length=3, blank=True, null=True)
    height = models.FloatField(blank=True, null=True, help_text="Height in meters")
    weight = models.FloatField(blank=True, null=True, help_text="Weight in kg")

    def __str__(self):
        return self.username

    def calculate_bmi(self):
        if self.height and self.weight:
            return round(self.weight / (self.height ** 2), 1)
        return None

    def calculate_caloric_needs(self):
        if self.gender and self.weight and self.height and self.age:
            if self.gender == 'Male':
                return int(10 * self.weight + 6.25 * self.height * 100 - 5 * self.age + 5)
            elif self.gender == 'Female':
                return int(10 * self.weight + 6.25 * self.height * 100 - 5 * self.age - 161)
        return None


from django.contrib.auth import get_user_model

User = get_user_model()

class DoctorApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensure CASCADE behavior
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    pmdc_number = models.CharField(max_length=50)
    experience = models.IntegerField()
    clinic_address = models.TextField()
    medical_certificate = models.FileField(upload_to="doctor_certificates/")
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.specialization}"


def save(self, *args, **kwargs):
    old_instance = None
    if self.pk:
        old_instance = DoctorApplication.objects.get(pk=self.pk)

    super().save(*args, **kwargs)

    if old_instance and old_instance.is_approved != self.is_approved:
        if self.is_approved:
            send_mail(
                'Application Approved',
                'Congratulations! Your application to become a doctor has been approved.',
                'admin@docsage.com',
                [self.email],
                fail_silently=False,
            )
        else:
            send_mail(
                'Application Rejected',
                'Unfortunately, your application to become a doctor has been rejected.',
                'admin@docsage.com',
                [self.email],
                fail_silently=False,
            )


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()  # e.g., 1 to 5 stars
    content = models.TextField()  # The review text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"Message by {self.sender.username} at {self.timestamp}"

