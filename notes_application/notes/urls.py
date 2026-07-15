from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("register/",views.register_view,name="register"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("add/",views.create_note,name="create_note"),
    path("update/<int:pk>/",views.update_note,name="update_note"),
    path("delete/<int:pk>/",views.delete_note,name="delete_note"),
]
