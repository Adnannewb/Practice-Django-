from django.urls import path,include
from .import views
urlpatterns = [
    path("",views.home,name='home'),
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
    path("register/",views.register_view,name='register'),
    path("dashboard/<int:pk>/",views.dashboard,name='dashboard'),
    path("image/upload/",views.image_upload,name='image_upload'),
    path("image/update/<int:pk>/",views.image_update,name='image_update'),
    path("image/delete/<int:pk>/",views.image_delete,name='image_delete'),
]