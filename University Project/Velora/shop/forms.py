from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category", "name", "description", "brand", "size", "color", "condition",
            "image", "image_2", "image_3",
            "price_per_day", "security_deposit", "quantity",
            "is_available", "is_featured", "is_hot_deal", "discount_percent",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("is_hot_deal") and not cleaned.get("discount_percent"):
            self.add_error(
                "discount_percent",
                "Set a discount percentage when this is marked as a Hot Deal.",
            )
        if (cleaned.get("discount_percent") or 0) > 90:
            self.add_error("discount_percent", "Discount cannot exceed 90%.")
        return cleaned