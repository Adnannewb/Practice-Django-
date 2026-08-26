from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from reviews.models import Review
from .forms import ProductForm
from .models import Category, Product


def home(request):
    featured = Product.objects.filter(is_available=True, is_featured=True)[:6]
    latest = Product.objects.filter(is_available=True)[:8]
    # Hot deals: explicit flag OR top by booking count — whichever yields the freshest mix.
    hot_deals = list(
        Product.objects.filter(is_available=True, is_hot_deal=True).order_by("-discount_percent", "-created_at")[:6]
    )
    trending = list(
        Product.objects.filter(is_available=True)
        .annotate(rentals_count=Count("rentals"))
        .order_by("-rentals_count", "-created_at")[:6]
    )
    # If we don't have explicit hot deals, fall back to trending so the section never looks empty.
    if not hot_deals:
        hot_deals = trending
    categories = Category.objects.all()[:8]
    context = {
        "featured": featured,
        "latest": latest,
        "hot_deals": hot_deals,
        "trending": trending,
        "categories": categories,
    }
    return render(request, "shop/home.html", context)


def product_list(request):
    qs = Product.objects.filter(is_available=True)
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q))
    if category:
        qs = qs.filter(category__slug=category)
    if sort == "trending":
        qs = qs.annotate(rc=Count("rentals")).order_by("-rc", "-created_at")
    elif sort == "price_low":
        qs = qs.order_by("price_per_day")
    elif sort == "price_high":
        qs = qs.order_by("-price_per_day")
    elif sort == "deals":
        qs = qs.filter(is_hot_deal=True).order_by("-discount_percent")
    context = {
        "products": qs,
        "categories": Category.objects.all(),
        "current_category": category,
        "q": q,
        "sort": sort,
    }
    return render(request, "shop/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = (
        Product.objects.filter(category=product.category, is_available=True)
        .exclude(pk=product.pk)
        .annotate(rc=Count("rentals"))
        .order_by("-rc", "-created_at")[:4]
    )
    reviews = product.reviews.select_related("customer").order_by("-created_at")
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(product=product, customer=request.user).exists()
    return render(request, "shop/product_detail.html", {
        "product": product, "related": related, "reviews": reviews,
        "user_has_reviewed": user_has_reviewed,
    })


@login_required
def product_create(request):
    # C2C: anyone with an account can list items from their wardrobe.
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, "Product listed!")
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm()
    return render(request, "shop/product_form.html", {"form": form, "title": "List a new item"})


@login_required
def product_edit(request, slug):
    product = get_object_or_404(Product, slug=slug, owner=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm(instance=product)
    return render(request, "shop/product_form.html", {"form": form, "title": "Edit product"})


@login_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug, owner=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product removed.")
        return redirect("shop:home")
    return render(request, "shop/product_confirm_delete.html", {"product": product})
