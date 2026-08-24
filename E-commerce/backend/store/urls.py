from django.urls import path,include
from .import views
urlpatterns = [
    
    path("product/", views.get_products),
    path("product/<int:id>/", views.get_product),
    path("category/", views.get_categories),
    
]
