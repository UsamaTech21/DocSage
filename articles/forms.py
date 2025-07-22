# articles/forms.py

from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags', 'feature_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control border-blue-500 shadow-md',
                'placeholder': 'Enter article title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control border-blue-500 shadow-md',
                'rows': 8,
                'placeholder': 'Enter article content',
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control border-blue-500 shadow-md',
                'placeholder': 'Enter article category',
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control border-blue-500 shadow-md',
                'placeholder': 'Enter tags separated by commas',
            }),
            'feature_image': forms.ClearableFileInput(attrs={
                'class': 'form-control border-blue-500 shadow-md',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control border-blue-500 shadow-md',
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control border-blue-500 shadow-md',
                'rows': 3,
                'placeholder': 'Write your comment here...',
            }),
        }
