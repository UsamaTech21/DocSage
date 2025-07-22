from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    expertise = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    contact_info = models.TextField()
    picture = models.ImageField(upload_to='doctor_pictures/', blank=True, null=True)

    def __str__(self):
        return self.name
