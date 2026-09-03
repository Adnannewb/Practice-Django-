from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Rating,Order

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "name@example.com"}),
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
    )

    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Choose a username"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Create a password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm password"}
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class RatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields=['rating','comment']
        widgets={
            'rating':forms.Select(choices=[(i,i)for i in range(1,6)]),
            'comment':forms.Textarea(attrs={'rows':4})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-select'})
        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Write your review here...'
        })

class CheckoutForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','email','address','postal_code','city','note']
        widgets={
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street address'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal code'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'note': forms.Textarea(attrs={'rows':4, 'class': 'form-control', 'placeholder': 'Add any special instructions or delivery notes here.'})
        }