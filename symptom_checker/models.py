from django.db import models
from django.contrib.auth import get_user_model

# Dynamically fetch the user model
User = get_user_model()

class Symptom(models.Model):
    body_part = models.CharField(max_length=100)
    possible_diseases = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to the User model
    image = models.ImageField(upload_to='symptoms/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body_part
    