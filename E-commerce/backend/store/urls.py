from django.urls import path,include
from .import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path("register/", views.register_view, name="register"),
    # for login 
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("product/", views.get_products),
    path("product/<int:id>/", views.get_product),
    path("category/", views.get_categories),
    path("cart/", views.get_cart),
    path("cart/add/", views.add_to_cart),
    path("cart/update/", views.update_cart_quantity),
    path("cart/remove/", views.remove_from_cart),
    path("orders/create/", views.create_order),
    
    
]
