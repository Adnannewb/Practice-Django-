from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Home,UserLoginView,UserProfileView,EventDetailView,AddEvent,DeleteEvent,UpdateEvent,SignUpView,EventRegister,cancel_registration,DashboardView
urlpatterns = [
    path("",Home.as_view(),name='home'),
    path("login/",UserLoginView.as_view(),name='login'),
    path("signup/",SignUpView.as_view(),name='signup'),
    path("logout/",LogoutView.as_view(),name='logout'),
    path("dashboard/",DashboardView.as_view(),name='dashboard'),
    path("profile/<int:pk>/",UserProfileView.as_view(),name='userprofile'),
    path("event-detail/<int:pk>",EventDetailView.as_view(),name='event_detail'),
    path("add_event/",AddEvent.as_view(),name='add_event'),
    path("update_event/<int:pk>/",UpdateEvent.as_view(),name='update_event'),
    path("delete_event/<int:pk>/",DeleteEvent.as_view(),name='delete_event'),
    path("event-register/",EventRegister.as_view(),name='event_Register'),
    path("cancel-registration/<int:pk>/",cancel_registration,name='cancel_registration'),
]