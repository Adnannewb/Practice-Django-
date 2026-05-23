from . import views
from django.urls import path,include

urlpatterns = [
    path("", views.feedback_form, name="feedback_form"),
]