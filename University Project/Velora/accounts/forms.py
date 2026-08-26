from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect, initial=User.ROLE_CUSTOMER)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "role", "phone", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "phone", "bio", "avatar")