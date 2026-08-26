from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    SIZE_CHOICES = [
        ("XS", "XS"), ("S", "S"), ("M", "M"),
        ("L", "L"), ("XL", "XL"), ("FREE", "Free Size"),
    ]
    CONDITION_CHOICES = [
        ("new", "New"),
        ("like_new", "Like New"),
        ("good", "Good"),
        ("used", "Used"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    brand = models.CharField(max_length=80, blank=True)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default="FREE")
    color = models.CharField(max_length=40, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default="like_new")

    image = models.ImageField(upload_to="products/")
    image_2 = models.ImageField(upload_to="products/", blank=True, null=True)
    image_3 = models.ImageField(upload_to="products/", blank=True, null=True)

    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # --- Trending / Hot deal ---
    is_hot_deal = models.BooleanField(
        default=False,
        help_text="Surface this product in the Hot Deals / Trending section on the home page.",
    )
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        help_text="Percent off the per-day price. 0 = no discount. Capped at 90.",
    )
    booking_count = models.PositiveIntegerField(
        default=0,
        help_text="How many times this product has been booked. Drives the trending ranking.",
        editable=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)[:50]
            slug = base
            i = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        # Cap discount so a typo can't break the maths.
        if self.discount_percent and self.discount_percent > 90:
            self.discount_percent = 90
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        """Price after discount, rounded to 2 decimals. Falls back to base price."""
        if self.discount_percent and self.discount_percent > 0:
            factor = (100 - self.discount_percent) / 100
            from decimal import Decimal, ROUND_HALF_UP
            return (self.price_per_day * Decimal(factor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return self.price_per_day

    @property
    def is_on_sale(self):
        return bool(self.discount_percent) and self.discount_percent > 0

    @property
    def average_rating(self):
        from django.db.models import Avg
        result = self.reviews.aggregate(avg=Avg("rating"))
        return round(result["avg"], 1) if result["avg"] else None

    @property
    def review_count(self):
        return self.reviews.count()
