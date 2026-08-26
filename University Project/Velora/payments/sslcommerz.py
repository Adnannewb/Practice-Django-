"""Thin wrapper around the sslcommerz-lib SDK with safe fallbacks."""
from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.conf import settings

try:
    from sslcommerz_lib import SSLCOMMERZ
except Exception:  # pragma: no cover
    SSLCOMMERZ = None


class SSLCommerzError(RuntimeError):
    pass


def _gateway():
    if SSLCOMMERZ is None:
        raise SSLCommerzError("sslcommerz-lib is not installed.")
    if not settings.SSLCOMMERZ_STORE_ID or not settings.SSLCOMMERZ_STORE_PASSWD:
        raise SSLCommerzError(
            "SSLCommerz credentials missing — set SSLCOMMERZ_STORE_ID and "
            "SSLCOMMERZ_STORE_PASSWD in your .env file."
        )
    # The sslcommerz-lib SDK builds the gateway/validation URLs from the
    # issandbox flag. The URLs configured in .env are kept for reference and
    # mirrored here in case the SDK is later swapped out.
    gateway = SSLCOMMERZ({
        "store_id": settings.SSLCOMMERZ_STORE_ID,
        "store_pass": settings.SSLCOMMERZ_STORE_PASSWD,
        "issandbox": settings.SSLCOMMERZ_IS_SANDBOX,
    })
    gateway.payment_url = settings.SSLCOMMERZ_PAYMENT_URL
    gateway.validation_url = settings.SSLCOMMERZ_VALIDATION_URL
    return gateway


def init_session(*, transaction_id: str, amount: Decimal | float, customer_name: str,
                 customer_email: str, customer_phone: str, product_name: str,
                 success_url: str, fail_url: str, cancel_url: str, ipn_url: str) -> dict[str, Any]:
    """Build the payload for an SSLCommerz session and call createSession."""
    payload = {
        "total_amount": float(amount),
        "currency": settings.SSLCOMMERZ_CURRENCY,
        "tran_id": transaction_id,
        "success_url": success_url,
        "fail_url": fail_url,
        "cancel_url": cancel_url,
        "ipn_url": ipn_url,
        "emi_option": 0,
        "cus_name": customer_name or "Customer",
        "cus_email": customer_email or "customer@example.com",
        "cus_add1": "Dhaka",
        "cus_city": "Dhaka",
        "cus_state": "Dhaka",
        "cus_postcode": "1000",
        "cus_country": "Bangladesh",
        "cus_phone": customer_phone or "01700000000",
        "shipping_method": "NO",
        "product_name": product_name,
        "product_category": "Fashion Rental",
        "product_profile": "general",
    }
    gateway = _gateway()
    response = gateway.createSession(payload)
    if isinstance(response, dict) and response.get("status") == "SUCCESS":
        return response
    raise SSLCommerzError(f"SSLCommerz init failed: {response}")


def validate_transaction(val_id: str) -> dict[str, Any]:
    """Server-side transaction validation."""
    return _gateway().validationTransaction(val_id)