from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CUSTOMER = "customer"
    ROLE_SELLER = "seller"
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Customer"),
        (ROLE_SELLER, "Seller"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    # In a true C2C marketplace, every user can list their own wardrobe AND rent
    # from others. We let sellers opt out of renting (they're focused on
    # lending) by flipping can_rent_items off; customers always default to True.
    can_rent_items = models.BooleanField(
        default=True,
        help_text="If False, the user cannot book rentals (lender-only mode).",
    )
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_seller(self):
        return self.role == self.ROLE_SELLER

    @property
    def is_customer(self):
        return self.role == self.ROLE_CUSTOMER

    @property
    def can_rent(self):
        """True when the user is allowed to book someone else's rental."""
        return self.can_rent_items and self.role == self.ROLE_CUSTOMER

    def save(self, *args, **kwargs):
        # Sellers are lenders by default; force can_rent_items off so the
        # marketplace stays strictly peer-to-peer (no B2C buying).
        if self.role == self.ROLE_SELLER:
            self.can_rent_items = False
        elif self.role == self.ROLE_CUSTOMER and not self.pk:
            # New customers default to renters.
            self.can_rent_items = True
        super().save(*args, **kwargs)
