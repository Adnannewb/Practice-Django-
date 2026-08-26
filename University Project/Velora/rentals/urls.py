from django.urls import path
from . import views

app_name = "rentals"

urlpatterns = [
    path("book/<slug:slug>/", views.book_product, name="book"),
    path("my/", views.my_rentals, name="my_rentals"),
    path("manage/", views.seller_rentals, name="seller_rentals"),
    path("<int:pk>/settle-deposit/", views.settle_deposit, name="settle_deposit"),
    path("<int:pk>/<str:action>/", views.update_status, name="update_status"),
    path("<int:pk>/", views.rental_detail, name="detail"),
]