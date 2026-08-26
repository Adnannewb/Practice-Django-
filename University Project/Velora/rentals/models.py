from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Rental(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_ACTIVE = "active"
    STATUS_RETURNED = "returned"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_RETURNED, "Returned"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rentals")
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE, related_name="rentals")

    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)

    rental_fee = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    note = models.TextField(blank=True)
    seller_message = models.TextField(blank=True)

    # --- Deposit settlement snapshot (filled when seller marks returned/completed) ---
    deposit_deducted = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_refunded = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit_settled_at = models.DateTimeField(blank=True, null=True)
    deposit_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")
        if self.start_date and self.start_date < date.today():
            raise ValidationError("Start date cannot be in the past.")

    @property
    def days(self):
        return max((self.end_date - self.start_date).days + 1, 1)

    @property
    def is_paid(self):
        return hasattr(self, "payment") and self.payment.status == "paid"

    @property
    def is_deposit_settled(self):
        return self.deposit_settled_at is not None

    def get_status_color(self):
        return {
            self.STATUS_PENDING: "warning",
            self.STATUS_APPROVED: "info",
            self.STATUS_REJECTED: "danger",
            self.STATUS_ACTIVE: "primary",
            self.STATUS_RETURNED: "secondary",
            self.STATUS_COMPLETED: "success",
            self.STATUS_CANCELLED: "dark",
        }.get(self.status, "secondary")

    def get_absolute_url(self):
        return reverse("rentals:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Rental #{self.pk} — {self.product.name} for {self.customer.username}"


class DepositSettlement(models.Model):
    """Audit log of each deposit decision a seller makes on a returned rental.

    One rental can have at most one settlement record — the fields on the Rental
    itself are the source of truth (deposit_deducted, deposit_refunded,
    deposit_settled_at, deposit_note). This table keeps a full history so a
    seller can later amend the decision without losing the original.
    """

    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name="settlements")
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="deposit_decisions"
    )
    damage_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Amount deducted from the deposit due to damage / loss.",
    )
    refunded_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Amount returned to the customer.",
    )
    note = models.TextField(blank=True, help_text="What happened? Visible to the customer.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def clean(self):
        # If the FK hasn't been linked yet (e.g. full_clean from a form before
        # the view assigns the rental), skip the deep validation — the form's
        # clean() handles it once the rental exists.
        if self.rental_id is None:
            return
        total = self.rental.security_deposit
        if (self.damage_amount or 0) + (self.refunded_amount or 0) > total:
            raise ValidationError(
                f"Deduction + refund ({self.damage_amount + self.refunded_amount}) "
                f"cannot exceed the security deposit ({total})."
            )
        if (self.damage_amount or 0) < 0 or (self.refunded_amount or 0) < 0:
            raise ValidationError("Amounts cannot be negative.")

    def __str__(self):
        return f"Settlement for Rental #{self.rental_id} — ৳{self.damage_amount} deducted"
