from django import forms
from .models import Comment
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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