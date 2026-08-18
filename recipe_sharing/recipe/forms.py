from .models import Recipe
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
        def cleaned_email(self):
            email=self.cleaned_data["email"]
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Email Already Exists !')
            return email
            


class RecipeForm(forms.ModelForm):
    class Meta:
        model=Recipe
        exclude = ['owner', 'created_at'] 