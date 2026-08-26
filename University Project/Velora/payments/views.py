import uuid
from urllib.parse import urljoin

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from rentals.models import Rental
from .models import Payment
from .sslcommerz import SSLCommerzError, init_session, validate_transaction


def _absolute(request, path: str) -> str:
    return request.build_absolute_uri(path)


@login_required
def checkout(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id, customer=request.user)
    payment, _ = Payment.objects.get_or_create(
        rental=rental,
        defaults={
            "transaction_id": f"VEL-{uuid.uuid4().hex[:10].upper()}",
            "amount": rental.total_amount,
            "currency": settings.SSLCOMMERZ_CURRENCY,
        },
    )
    if payment.status == Payment.STATUS_PAID:
        messages.info(request, "This rental is already paid.")
        return redirect("rentals:detail", pk=rental.pk)

    if request.method == "POST":
        try:
            response = init_session(
                transaction_id=payment.transaction_id,
                amount=payment.amount,
                customer_name=request.user.get_full_name() or request.user.username,
                customer_email=request.user.email,
                customer_phone=request.user.phone or "01700000000",
                product_name=rental.product.name,
                success_url=_absolute(request, reverse("payments:success")),
                fail_url=_absolute(request, reverse("payments:fail")),
                cancel_url=_absolute(request, reverse("payments:cancel")),
                ipn_url=_absolute(request, reverse("payments:ipn")),
            )
        except SSLCommerzError as e:
            messages.error(request, str(e))
            return redirect("rentals:detail", pk=rental.pk)

        payment.status = Payment.STATUS_PENDING
        payment.raw_response = response
        payment.save()
        gateway_url = response.get("GatewayPageURL")
        if not gateway_url:
            messages.error(request, "Could not get gateway URL.")
            return redirect("rentals:detail", pk=rental.pk)
        return redirect(gateway_url)

    return render(request, "payments/checkout.html", {"rental": rental, "payment": payment})


@csrf_exempt
def payment_success(request):
    tran_id = request.POST.get("tran_id") or request.GET.get("tran_id")
    val_id = request.POST.get("val_id") or request.GET.get("val_id")
    payment = get_object_or_404(Payment, transaction_id=tran_id)
    payment.val_id = val_id
    payment.bank_tran_id = request.POST.get("bank_tran_id", "")
    payment.card_type = request.POST.get("card_type", "")
    payment.raw_response = {k: v for k, v in request.POST.items()}
    payment.status = Payment.STATUS_PAID
    payment.save()
    payment.rental.status = Rental.STATUS_APPROVED
    payment.rental.save()
    messages.success(request, "Payment successful! Your rental is confirmed.")
    return render(request, "payments/success.html", {"payment": payment})


@csrf_exempt
def payment_fail(request):
    tran_id = request.POST.get("tran_id") or request.GET.get("tran_id")
    payment = get_object_or_404(Payment, transaction_id=tran_id)
    payment.status = Payment.STATUS_FAILED
    payment.raw_response = {k: v for k, v in request.POST.items()}
    payment.save()
    return render(request, "payments/fail.html", {"payment": payment})


@csrf_exempt
def payment_cancel(request):
    tran_id = request.POST.get("tran_id") or request.GET.get("tran_id")
    payment = get_object_or_404(Payment, transaction_id=tran_id)
    payment.status = Payment.STATUS_CANCELLED
    payment.save()
    return render(request, "payments/cancel.html", {"payment": payment})


@csrf_exempt
def payment_ipn(request):
    """Server-to-server validation — runs after the user returns."""
    tran_id = request.POST.get("tran_id")
    val_id = request.POST.get("val_id")
    if not tran_id or not val_id:
        return HttpResponse(status=400)
    try:
        payment = Payment.objects.get(transaction_id=tran_id)
        result = validate_transaction(val_id)
        payment.raw_response = result
        if result.get("status") == "VALID" or result.get("VALID") == "VALID":
            payment.status = Payment.STATUS_PAID
            payment.rental.status = Rental.STATUS_APPROVED
            payment.rental.save()
        else:
            payment.status = Payment.STATUS_FAILED
        payment.save()
    except Exception as e:  # pragma: no cover
        return HttpResponse(f"IPN error: {e}", status=500)
    return HttpResponse("OK")
