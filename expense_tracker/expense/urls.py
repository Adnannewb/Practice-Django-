from django.urls import path
from .import views

urlpatterns = [
    path("",views.expenses_list,name="expenses_list"),
    path("add/",views.add_expense,name="add_expense"),
    path("update/<int:pk>/",views.update_expense,name="update_expense"),
    path("delete/<int:pk>/",views.delete_expense,name="delete_expense"),
]