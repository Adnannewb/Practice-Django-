from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Employee(models.Model):

    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )

    name = models.CharField(max_length=100)

    department = models.CharField(max_length=100)

    salary = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    joining_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    def __str__(self):
        return self.name