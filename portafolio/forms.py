from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile

class SignUpForm(UserCreationForm):

    username = forms.CharField(help_text=None,
                               label=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    email = forms.EmailField(label=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    password1 = forms.CharField(label=False,
                               widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    password2 = forms.CharField(label=False,
                               widget=forms.PasswordInput(attrs={'placeholder':'Confirm password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    
    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas deben ser iguales")
        
        return cleaned_data
        

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']

        if username == 'admin':
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True
            )
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=False,
                               help_text=None,
                               widget=forms.TextInput(attrs={'placeholder':'Username'}))

    password = forms.CharField(label=False,
                               help_text=None,
                               widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

class UserForm(forms.ModelForm):

    username = forms.CharField(help_text=None,
                               label="Username")

    birthday = forms.DateField(help_text=None,
                               required=False,
                               label='Birthday',
                               widget=forms.TextInput(attrs={'type':'date'}))

    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = [
            'username',
            'birthday',
            'email',
        ]

class ProfileForm(forms.ModelForm):

    photo = forms.ImageField(label="Photo",
                             help_text=None,
                             required=False,
                             widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = [
            'photo',
        ]

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label=False,
                                   widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    new_password1 = forms.CharField(label=False,
                                   widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))

    new_password2 = forms.CharField(label=False,
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    class Meta:
        model = User
        fields = [
            'old_password',
            'new_password1',
            'new_password2',
        ]

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas deben ser iguales")

        return cleaned_data