from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render
from .forms import LoginForm, ProfileForm, SignUpForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Velora, {user.username}!")
            return redirect("shop:home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("shop:home")
    else:
        form = LoginForm(request)
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("shop:home")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def dashboard_view(request):
    """Landing page after login — shows listings + rentals in a C2C layout."""
    from shop.models import Product
    from rentals.models import Rental

    user = request.user
    context = {
        "user_obj": user,
        "products": Product.objects.filter(owner=user).order_by("-created_at"),
    }
    if user.can_rent:
        rentals_qs = Rental.objects.filter(customer=user).order_by("-created_at")
        context["rentals"] = rentals_qs
        agg = rentals_qs.aggregate(
            total_deposit=Sum("security_deposit"),
            total_refunded=Sum("deposit_refunded"),
            total_charged=Sum("deposit_deducted"),
        )
        context["deposit_summary"] = {
            "total_deposit": agg["total_deposit"] or 0,
            "total_refunded": agg["total_refunded"] or 0,
            "total_charged": agg["total_charged"] or 0,
        }
    return render(request, "accounts/dashboard.html", context)
