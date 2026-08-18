from django.urls import path
from .import views
urlpatterns = [
    path("",views.home,name='home'),
    path("register/",views.register_view,name='register'),
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
    path("dashboard/<int:pk>/",views.dashboard,name='dashboard'),
    path("add_recipe/",views.add_recipe,name='add_recipe'),
    path("update_recipe/<int:pk>/",views.update_recipe,name='update_recipe'),
    path("delete_recipe/<int:pk>/",views.delete_recipe,name='delete_recipe'),
    
]