from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "owner", "category", "price_per_day",
        "is_available", "is_featured", "is_hot_deal", "discount_percent",
        "booking_count", "created_at",
    )
    list_filter = ("is_available", "is_featured", "is_hot_deal", "category", "condition")
    search_fields = ("name", "brand", "description", "owner__username")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("booking_count",)
