from . import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register("reviews",views.ReviewViewset,basename="reviews")
urlpatterns = [
    
    path("", include(router.urls)),
]
