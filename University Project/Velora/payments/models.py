from django.db import models
from rentals.models import Rental


class Payment(models.Model):
    STATUS_INITIATED = "initiated"
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_CANCELLED = "cancelled"
    STATUS_REFUNDED = "refunded"
    STATUS_CHOICES = [
        (STATUS_INITIATED, "Initiated"),
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_REFUNDED, "Refunded"),
    ]

    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, related_name="payment")
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="BDT")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_INITIATED)

    # raw gateway response fields
    val_id = models.CharField(max_length=100, blank=True)
    bank_tran_id = models.CharField(max_length=100, blank=True)
    card_type = models.CharField(max_length=50, blank=True)
    raw_response = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Payment {self.transaction_id} ({self.status})"
