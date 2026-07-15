from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Choose a username',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Create a password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm your password',
        })

    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Exists")
        return email
            
    
    
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter book title',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter author name',
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter publisher name',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter price',
                'step': '0.01',
                'min': '0',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter quantity',
                'min': '0',
            }),
        }
    