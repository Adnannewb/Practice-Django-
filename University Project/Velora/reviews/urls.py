from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("add/<slug:slug>/", views.add_review, name="add"),
    path("<int:pk>/delete/", views.delete_review, name="delete"),
]