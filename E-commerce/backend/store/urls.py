from django.urls import path,include
from .import views
urlpatterns = [
    
    path("product/", views.get_products),
    path("product/<int:id>/", views.get_product),
    path("category/", views.get_categories),
    path("cart/", views.get_cart),
    path("cart/add/", views.add_to_cart),
    path("cart/remove/", views.remove_from_cart),
    
]
