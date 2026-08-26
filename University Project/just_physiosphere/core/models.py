from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('therapist', 'Therapist'),
        ('admin', 'Admin'),
    ]
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


class Service(models.Model):
    name = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='therapist_profile')
    qualifications = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    # NEW: uploaded photo
    photo = models.ImageField(upload_to='therapist_photos/', null=True, blank=True)

    # existing URL field (optional, kept for backward compatibility)
    photo_url = models.URLField(blank=True)

    daily_limit = models.PositiveIntegerField(default=12)
    unavailable_dates = models.JSONField(default=list, blank=True)  # list of ISO dates

    # already added earlier: which services this therapist provides
    services = models.ManyToManyField(Service, related_name='therapists', blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Payment(models.Model):
    METHOD_CHOICES = [
        ('online', 'Online'),
        ('cash', 'Cash'),
    ]
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    appointment = models.OneToOneField('Appointment', on_delete=models.CASCADE, related_name='payment', null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    txn_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.TextField(blank=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending_online_payment', 'Pending Online Payment'),
        ('pending_offline_verification', 'Pending Offline Verification'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('refunded', 'Refunded'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_online_payment')
    payment_method = models.CharField(max_length=20, default='online')
    attended = models.BooleanField(default=False)
    payment_id = models.IntegerField(null=True, blank=True)  # redundant but per requirement

    class Meta:
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['therapist', 'start_time']),
            models.Index(fields=['start_time', 'end_time']),
        ]

    def __str__(self):
        return f"{self.patient} with {self.therapist} at {self.start_time}"


class MedicalCard(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medical_card')
    summary = models.TextField(blank=True)

    def __str__(self):
        return f"Medical Card for {self.patient}"


class Visit(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='visits')
    notes = models.TextField(blank=True)
    attachment = models.FileField(upload_to='visit_attachments/', null=True, blank=True)
    signed = models.BooleanField(default=False)

    def __str__(self):
        return f"Visit for {self.appointment_id}"


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.subject} from {self.name}"


class AuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    target_table = models.CharField(max_length=100)
    target_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.action}"