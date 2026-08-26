from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from shop.models import Product
from .forms import DepositSettlementForm, RentalBookingForm
from .models import DepositSettlement, Rental


@login_required
@transaction.atomic
def book_product(request, slug):
    product = get_object_or_404(
        Product.objects.select_for_update(), slug=slug, is_available=True
    )
    # C2C: anyone can list their wardrobe, but only customers can book rentals.
    if not request.user.can_rent:
        messages.error(request, "Your account is in lender-only mode and cannot rent items.")
        return redirect(product.get_absolute_url())
    if product.owner_id == request.user.id:
        messages.error(request, "You cannot rent your own product.")
        return redirect(product.get_absolute_url())

    if request.method == "POST":
        form = RentalBookingForm(request.POST, product=product)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.customer = request.user
            rental.product = product
            rental.rental_fee = product.price_per_day * rental.days * rental.quantity
            rental.security_deposit = product.security_deposit * rental.quantity
            rental.total_amount = rental.rental_fee + rental.security_deposit
            try:
                rental.full_clean()
            except Exception as e:
                form.add_error(None, e)
            else:
                rental.save()
                messages.success(request, "Rental request submitted. Proceed to payment.")
                return redirect("payments:checkout", rental_id=rental.pk)
    else:
        form = RentalBookingForm(product=product)
    return render(request, "rentals/book.html", {"form": form, "product": product})


@login_required
def rental_detail(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    if rental.customer_id != request.user.id and rental.product.owner_id != request.user.id and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this rental.")
        return redirect("shop:home")
    return render(request, "rentals/detail.html", {"rental": rental})


@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "rentals/my_rentals.html", {"rentals": rentals})


@login_required
def seller_rentals(request):
    # C2C: anyone who has listed items needs to manage incoming bookings.
    # We check that the user actually owns at least one product rather than
    # gating on role.
    if not request.user.products.exists():
        messages.info(request, "You haven't listed any items yet.")
        return redirect("shop:home")
    rentals = Rental.objects.filter(product__owner=request.user).order_by("-created_at")
    return render(request, "rentals/seller_rentals.html", {"rentals": rentals})


@login_required
def update_status(request, pk, action):
    rental = get_object_or_404(Rental, pk=pk)
    is_seller = rental.product.owner_id == request.user.id
    is_customer = rental.customer_id == request.user.id
    if not (is_seller or is_customer or request.user.is_staff):
        messages.error(request, "Not allowed.")
        return redirect("shop:home")

    transitions = {
        "approve": (Rental.STATUS_APPROVED, "seller", "Rental approved."),
        "reject": (Rental.STATUS_REJECTED, "seller", "Rental rejected."),
        "ship": (Rental.STATUS_ACTIVE, "seller", "Rental marked as active."),
        "return": (Rental.STATUS_RETURNED, "seller", "Marked as returned."),
        "complete": (Rental.STATUS_COMPLETED, "seller", "Rental completed."),
        "cancel": (Rental.STATUS_CANCELLED, "customer", "Rental cancelled."),
    }
    if action not in transitions:
        messages.error(request, "Unknown action.")
        return redirect(rental.get_absolute_url())

    new_status, who, msg = transitions[action]
    if who == "seller" and not is_seller and not request.user.is_staff:
        messages.error(request, "Only the seller can perform that.")
        return redirect(rental.get_absolute_url())
    if who == "customer" and not is_customer and not request.user.is_staff:
        messages.error(request, "Only the renter can cancel.")
        return redirect(rental.get_absolute_url())

    # Don't let seller mark 'completed' until they've settled the deposit.
    if action == "complete" and not rental.is_deposit_settled:
        messages.warning(
            request,
            "Settle the security deposit first — refund the customer in full or "
            "record a damage charge, then mark complete.",
        )
        return redirect(rental.get_absolute_url())

    if request.method == "POST":
        rental.status = new_status
        rental.save()
        messages.success(request, msg)
    return redirect(rental.get_absolute_url())


@login_required
@transaction.atomic
def settle_deposit(request, pk):
    """Seller decides what happens to the deposit once the rental is back.

    - Must be the product's owner.
    - Rental must be in 'returned' status.
    - Cannot be settled twice.
    Records a DepositSettlement audit row and snapshots the figures onto the
    Rental itself for fast dashboard queries.
    """
    rental = get_object_or_404(Rental.objects.select_for_update(), pk=pk)
    if rental.product.owner_id != request.user.id and not request.user.is_staff:
        messages.error(request, "Only the seller can settle the deposit.")
        return redirect(rental.get_absolute_url())
    if rental.status != Rental.STATUS_RETURNED:
        messages.warning(request, "Deposit can only be settled once the rental is returned.")
        return redirect(rental.get_absolute_url())
    if rental.is_deposit_settled:
        messages.info(request, "This deposit has already been settled.")
        return redirect(rental.get_absolute_url())

    if request.method == "POST":
        form = DepositSettlementForm(request.POST, rental=rental)
        if form.is_valid():
            settlement = form.save(commit=False)
            settlement.rental = rental
            settlement.decided_by = request.user
            try:
                settlement.full_clean()
            except Exception as e:
                form.add_error(None, e)
            else:
                settlement.save()
                # snapshot onto rental
                rental.deposit_deducted = settlement.damage_amount
                rental.deposit_refunded = settlement.refunded_amount
                rental.deposit_settled_at = timezone.now()
                rental.deposit_note = settlement.note
                rental.save(update_fields=[
                    "deposit_deducted", "deposit_refunded",
                    "deposit_settled_at", "deposit_note", "updated_at",
                ])
                if settlement.damage_amount and settlement.damage_amount > 0:
                    messages.warning(
                        request,
                        f"Deposit settled — ৳{settlement.refunded_amount} refunded, "
                        f"৳{settlement.damage_amount} charged for damage.",
                    )
                else:
                    messages.success(request, f"Deposit fully refunded (৳{settlement.refunded_amount}).")
                return redirect(rental.get_absolute_url())
    else:
        form = DepositSettlementForm(rental=rental)
    return render(request, "rentals/settle_deposit.html", {"rental": rental, "form": form})
