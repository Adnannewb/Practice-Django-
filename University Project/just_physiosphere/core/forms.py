from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Appointment, Message, Therapist, Visit, Service


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'phone', 'password1', 'password2'
        )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email'].lower()
        user.email = email
        user.phone = self.cleaned_data['phone']
        user.role = 'patient'
        if email.endswith('@student.just.edu.bd'):
            user.is_student = True
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username")


class AppointmentForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=[('online', 'Online'), ('cash', 'Cash')]
    )

    class Meta:
        model = Appointment
        fields = ['therapist', 'service', 'start_time']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all()
        self.fields['therapist'].queryset = Therapist.objects.all()
        self.user = user
        # start_time is set by JS when a time slot is chosen
        self.fields['start_time'].widget = forms.HiddenInput()


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'message']


class TherapistProfileForm(forms.ModelForm):
    # Multi-select dropdown for services
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': 5}),
        required=False,
        help_text="Hold Ctrl (Windows) or Cmd (macOS) to select multiple services."
    )

    class Meta:
        model = Therapist
        fields = [
            'qualifications',
            'specialization',
            'bio',
            'photo',       # NEW: uploaded photo
            'photo_url',   # existing URL
            'daily_limit',
            'services',
        ]


class TherapistUnavailableForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['unavailable_dates']


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['notes', 'attachment', 'signed']