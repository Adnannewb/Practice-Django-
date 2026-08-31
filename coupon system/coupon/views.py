from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Coupon, Order
from .serializers import (
    CouponSerializer,
    OrderSerializer,
    ApplyCouponSerializer,
)


class CouponViewSet(viewsets.ModelViewSet):

    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):

        subtotal = serializer.validated_data["subtotal"]

        serializer.save(
            subtotal=subtotal,
            total_amount=subtotal
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="apply-coupon"
    )
    @transaction.atomic
    def apply_coupon(self, request, pk=None):

        # Lock the order
        order = Order.objects.select_for_update().get(
            pk=pk
        )

        serializer = ApplyCouponSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        coupon_code = serializer.validated_data[
            "coupon_code"
        ]

        # Lock coupon to prevent race conditions
        try:

            coupon = Coupon.objects.select_for_update().get(
                code=coupon_code
            )

        except Coupon.DoesNotExist:

            return Response(
                {
                    "detail": "Invalid coupon code."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 1. Check if coupon is active
        # -----------------------------------

        if not coupon.is_active:

            return Response(
                {
                    "detail": "This coupon is inactive."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 2. Check expiry
        # -----------------------------------

        if coupon.expiry_date <= timezone.now():

            return Response(
                {
                    "detail": "This coupon has expired."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 3. Check usage limit
        # -----------------------------------

        if coupon.used_count >= coupon.usage_limit:

            return Response(
                {
                    "detail": "This coupon has reached its usage limit."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 4. Check minimum order
        # -----------------------------------

        if order.subtotal < coupon.minimum_order:

            return Response(
                {
                    "detail": (
                        f"Minimum order amount for this coupon "
                        f"is {coupon.minimum_order}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 5. Calculate discount
        # -----------------------------------

        if coupon.discount_type == Coupon.DiscountType.PERCENTAGE:

            discount_amount = (
                order.subtotal *
                coupon.discount_value /
                Decimal("100")
            )

        elif coupon.discount_type == Coupon.DiscountType.FIXED:

            discount_amount = coupon.discount_value

        else:

            return Response(
                {
                    "detail": "Invalid discount type."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------
        # 6. Discount cannot exceed order
        # -----------------------------------

        if discount_amount > order.subtotal:

            discount_amount = order.subtotal

        # -----------------------------------
        # 7. Calculate final amount
        # -----------------------------------

        final_amount = (
            order.subtotal -
            discount_amount
        )

        # -----------------------------------
        # 8. Update order
        # -----------------------------------

        order.discount_amount = discount_amount
        order.total_amount = final_amount
        order.coupon = coupon

        order.save(
            update_fields=[
                "discount_amount",
                "total_amount",
                "coupon",
            ]
        )

        # -----------------------------------
        # 9. Increase coupon usage
        # -----------------------------------

        coupon.used_count += 1

        coupon.save(
            update_fields=[
                "used_count"
            ]
        )

        return Response(
            {
                "message": "Coupon applied successfully.",
                "coupon": coupon.code,
                "subtotal": order.subtotal,
                "discount": discount_amount,
                "total": final_amount,
            },
            status=status.HTTP_200_OK
        )