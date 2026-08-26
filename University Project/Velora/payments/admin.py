from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "rental", "amount", "currency", "status", "created_at")
    list_filter = ("status", "currency")
    search_fields = ("transaction_id", "val_id", "bank_tran_id", "rental__customer__username")
    readonly_fields = ("transaction_id", "created_at", "updated_at", "raw_response")
