from django.contrib import admin
from .models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "customer", "start_date", "end_date", "status", "total_amount", "created_at")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("product__name", "customer__username")
    readonly_fields = ("created_at", "updated_at")
