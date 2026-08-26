from datetime import date

from django import forms
from django.db.models import Q
from .models import Rental, DepositSettlement


# Statuses that actively hold inventory. Cancelled, rejected and (eventually)
# refunded rentals free their stock back up — they don't block new bookings.
_HOLDING_STATUSES = (
    Rental.STATUS_PENDING,
    Rental.STATUS_APPROVED,
    Rental.STATUS_ACTIVE,
    Rental.STATUS_RETURNED,
)


class RentalBookingForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ("start_date", "end_date", "quantity", "note")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "min": date.today().isoformat()}),
            "end_date": forms.DateInput(attrs={"type": "date", "min": date.today().isoformat()}),
        }

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._product = product

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")
        qty = cleaned.get("quantity") or 1
        product = self._product or getattr(self.instance, "product", None)

        if start and end and end < start:
            raise forms.ValidationError("End date must be on or after start date.")

        if not product:
            return cleaned

        # Total stock check (per-product cap, regardless of dates).
        if qty > product.quantity:
            raise forms.ValidationError(
                f"Only {product.quantity} unit(s) of this item exist — "
                f"please request {product.quantity} or fewer."
            )

        if start and end:
            # Sum quantity of all *other* rentals whose dates overlap and which
            # still hold stock. Cancellation / rejection release inventory.
            overlapping = (
                Rental.objects
                .filter(product=product, status__in=_HOLDING_STATUSES)
                .filter(start_date__lte=end, end_date__gte=start)
            )
            if self.instance.pk:
                overlapping = overlapping.exclude(pk=self.instance.pk)
            booked = sum(r.quantity for r in overlapping)
            remaining = product.quantity - booked
            if qty > remaining:
                if remaining <= 0:
                    raise forms.ValidationError(
                        "Sorry — this item is fully booked across the entire "
                        "date range you selected. Pick different dates."
                    )
                raise forms.ValidationError(
                    f"Only {remaining} unit(s) left for those dates "
                    f"({booked} already booked, {product.quantity} in stock)."
                )
        return cleaned


class DepositSettlementForm(forms.ModelForm):
    """Seller uses this when a returned rental needs damage / refund evaluation."""

    class Meta:
        model = DepositSettlement
        fields = ("damage_amount", "refunded_amount", "note")
        widgets = {
            "damage_amount": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "refunded_amount": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
            "note": forms.Textarea(attrs={"rows": 3, "placeholder": "Describe what happened. Customer can read this."}),
        }

    def __init__(self, *args, rental=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._rental = rental
        if rental:
            self.fields["refunded_amount"].initial = rental.security_deposit
            self.fields["refunded_amount"].help_text = (
                f"Default = full deposit ৳{rental.security_deposit}. "
                f"Reduce it to charge for damage / loss."
            )

    def clean(self):
        cleaned = super().clean()
        if not self._rental:
            return cleaned
        damage = cleaned.get("damage_amount") or 0
        refund = cleaned.get("refunded_amount") or 0
        if damage < 0 or refund < 0:
            raise forms.ValidationError("Amounts cannot be negative.")
        deposit = self._rental.security_deposit
        if damage + refund > deposit:
            raise forms.ValidationError(
                f"Deduction (৳{damage}) + refund (৳{refund}) cannot exceed the "
                f"deposit held (৳{deposit}). The customer paid ৳{deposit} up front."
            )
        return cleaned