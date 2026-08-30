from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path,include

router=DefaultRouter()
router.register("register",views.RegistrationViewset,'registrations')

urlpatterns = [
   
    path("",include(router.urls)),
]