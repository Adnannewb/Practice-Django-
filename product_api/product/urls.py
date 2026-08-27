from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('product',views.ProductModelViwsets,'product')
urlpatterns = [

    # path("get_product/",views.get_product),
    # path("add_product/",views.add_product),
    # path("update_product/<int:pk>",views.edit_delete_product),
    path('',include(router.urls)),
]
