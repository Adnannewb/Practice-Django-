from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Coupon, Order


class CouponSerializer(serializers.ModelSerializer):

    code = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Coupon.objects.all(),
                message="Coupon already exists."
            )
        ]
    )

    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ["used_count"]

    def validate_code(self, value):

        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Coupon code cannot be empty."
            )

        return value

    def validate_expiry_date(self, value):

        if value <= timezone.now():
            raise serializers.ValidationError(
                "Expiry date must be in the future."
            )

        return value

    def validate_discount_value(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Discount value must be greater than zero."
            )

        return value

    def validate_minimum_order(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Minimum order cannot be negative."
            )

        return value

    def validate_usage_limit(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Usage limit must be greater than zero."
            )

        return value

    def validate(self, attrs):

        discount_type = attrs.get("discount_type")
        discount_value = attrs.get("discount_value")

        if discount_type == Coupon.DiscountType.PERCENTAGE:

            if discount_value > Decimal("100"):
                raise serializers.ValidationError({
                    "discount_value":
                        "Percentage discount cannot exceed 100%."
                })

        return attrs


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "id",
            "subtotal",
            "discount_amount",
            "total_amount",
            "coupon",
            "created_at",
        ]

        read_only_fields = [
            "discount_amount",
            "total_amount",
            "coupon",
            "created_at",
        ]

    def validate_subtotal(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Order amount must be greater than zero."
            )

        return value


class ApplyCouponSerializer(serializers.Serializer):

    coupon_code = serializers.CharField(
        max_length=50
    )

    def validate_coupon_code(self, value):

        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Coupon code cannot be empty."
            )

        return value