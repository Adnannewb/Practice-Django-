from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Product
from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    review = Review.objects.filter(product=product, customer=request.user).first()
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.product = product
            obj.customer = request.user
            obj.save()
            messages.success(request, "Thanks for your review!")
            return redirect(product.get_absolute_url())
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/add.html", {"form": form, "product": product})


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, customer=request.user)
    product = review.product
    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted.")
    return redirect(product.get_absolute_url())
