from django.urls import path
from .import views

urlpatterns = [
    path('send_mail/',views.send_test_mail,name='test_mail'),
    path('send_email/',views.send_test_email,name='test_email'),
    path('send_bulk_email/',views.send_test_bulk_email,name='test_bulk_email'),
]
