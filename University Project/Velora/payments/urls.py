from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/<int:rental_id>/", views.checkout, name="checkout"),
    path("success/", views.payment_success, name="success"),
    path("fail/", views.payment_fail, name="fail"),
    path("cancel/", views.payment_cancel, name="cancel"),
    path("ipn/", views.payment_ipn, name="ipn"),
]