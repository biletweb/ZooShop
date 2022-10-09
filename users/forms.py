from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from users.models import UserProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Введите логин:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Введите пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Введите e-mail:', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Введите своё имя:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Введите свою фамилию:', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'profile_pic')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'})
        }
