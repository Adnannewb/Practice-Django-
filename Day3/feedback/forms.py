from django import forms
from .models import Feedback    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['name','email','message']
        widgets={
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email'
            }),

            'message': forms.Textarea(attrs={
                'placeholder': 'Write your message',
                'rows': 5
            }),
        }
    
