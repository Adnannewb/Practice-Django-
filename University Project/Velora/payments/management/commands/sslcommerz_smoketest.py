"""Smoke-test the SSLCommerz sandbox credentials.

Usage:
    python manage.py sslcommerz_smoketest
"""
import uuid

from django.conf import settings
from django.core.management.base import BaseCommand

from payments.sslcommerz import SSLCommerzError, init_session


class Command(BaseCommand):
    help = "Verify SSLCommerz sandbox credentials can open a session."

    def handle(self, *args, **options):
        self.stdout.write("Store ID: %s" % settings.SSLCOMMERZ_STORE_ID)
        self.stdout.write("Sandbox : %s" % settings.SSLCOMMERZ_IS_SANDBOX)
        self.stdout.write("Gateway : %s" % settings.SSLCOMMERZ_PAYMENT_URL)

        try:
            resp = init_session(
                transaction_id=f"SMOKE-{uuid.uuid4().hex[:8].upper()}",
                amount=10.0,
                customer_name="Velora Tester",
                customer_email="test@example.com",
                customer_phone="01700000000",
                product_name="Smoke test product",
                success_url="http://127.0.0.1:8000/payments/success/",
                fail_url="http://127.0.0.1:8000/payments/fail/",
                cancel_url="http://127.0.0.1:8000/payments/cancel/",
                ipn_url="http://127.0.0.1:8000/payments/ipn/",
            )
        except SSLCommerzError as e:
            self.stderr.write(self.style.ERROR(f"FAILED: {e}"))
            return

        if resp.get("status") == "SUCCESS":
            self.stdout.write(self.style.SUCCESS("Session opened successfully."))
            self.stdout.write("Gateway URL: %s" % resp.get("GatewayPageURL"))
        else:
            self.stderr.write(self.style.WARNING(f"Unexpected response: {resp}"))