from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DoctorApplication

class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False, help_text="Upload a profile picture (optional).")
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'age', 'gender', 'blood_group', 'height', 'weight']

class JoinDoctorForm(forms.ModelForm):
    class Meta:
        model = DoctorApplication
        exclude = ['user', 'is_approved', 'submitted_at']


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'Write your review here...',
                    'rows': 4,
                    'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
                }
            ),
            'rating': forms.RadioSelect(
                choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]
            ),
        }
