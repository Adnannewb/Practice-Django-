from rest_framework import serializers
from .models import Product, Purchase, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'product', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):

        request = self.context['request']
        user = request.user
        product = attrs['product']

        # Product must be active
        if not product.is_active:
            raise serializers.ValidationError(
                "You cannot review an inactive product."
            )

        # User must have purchased the product
        if not Purchase.objects.filter(
            user=user,
            product=product
        ).exists():
            raise serializers.ValidationError(
                "You can only review products you have purchased."
            )

        # Only check duplicate when creating a review
        if self.instance is None:

            if Review.objects.filter(
                reviewer=user,
                product=product
            ).exists():
                raise serializers.ValidationError(
                    "You have already reviewed this product."
                )

        return attrs

    def create(self, validated_data):
        request = self.context['request']

        validated_data['reviewer'] = request.user

        return Review.objects.create(**validated_data)