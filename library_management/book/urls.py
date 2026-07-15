from .import views
from django.urls import path

urlpatterns = [
    path("",views.home,name='home'),
    path("add/",views.add_book,name='add_book'),
    path("dashboard/",views.dashboard,name='dashboard'),
    path("login/",views.login_view,name='login'),
    path("register/",views.register_view,name='register'),
    path("logout/",views.logout_view,name='logout'),
    path("details/<int:pk>/",views.book_details,name='book_details'),
    path("update/<int:pk>/",views.update_book,name='update_book'),
    path("delete/<int:pk>/",views.delete_book,name='delete_book'),
]