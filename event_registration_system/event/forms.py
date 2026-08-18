from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Registration,UserProfile,Event,Category


class SignUpForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Already Exists')
        return email
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['phone','address','dob','profile_picture']
        widgets={
            'dob': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }
        

class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        exclude=['organizer','created_at']
        widgets={
            'date':forms.DateTimeInput(
                attrs={'type':'datetime-local','class':'form-control'}
            ),
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=Registration
        fields=['event']

    