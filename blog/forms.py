from django import forms
from .models import Comment, Post
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_published': 'Опубликовать сразу',
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    captcha = CaptchaField(label="Проверка:")
    
    class Meta:
        model = Comment
        fields = ['author','email', 'text']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com (не публикуется, только для уведомлений)'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ваш комментарий...'
            }),
        }
        labels = {
            'author': 'Имя',
            'email': 'Email',
            'text': 'Комментарий',
        }