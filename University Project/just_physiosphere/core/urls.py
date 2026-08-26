from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_view, name='services'),
    path('about/', views.about_view, name='about'),
    path('faq/', views.faq_view, name='faq'),
    path('contact/', views.contact_view, name='contact'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path(
        'dashboard/user/cancel/<int:appointment_id>/',
        views.user_cancel_appointment,
        name='user_cancel_appointment',
    ),
    path(
        'dashboard/user/reschedule/<int:appointment_id>/',
        views.user_reschedule_appointment,
        name='user_reschedule_appointment',
    ),

    # Therapist dashboard + visit editing
    path('dashboard/therapist/', views.therapist_dashboard, name='therapist_dashboard'),
    path(
        'dashboard/therapist/visit/<int:appointment_id>/',
        views.therapist_edit_visit,
        name='therapist_edit_visit',
    ),

    # Admin dashboard + admin actions
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path(
        'dashboard/admin/toggle-therapist/<int:user_id>/',
        views.admin_toggle_therapist,
        name='admin_toggle_therapist',
    ),
    path(
        'dashboard/admin/services/create/',
        views.admin_service_crud,
        name='admin_service_create',
    ),

    # APIs
    path('api/therapist-services/', views.api_therapist_services, name='api_therapist_services'),
    path('api/available-slots/', views.api_available_slots, name='api_available_slots'),
    path('api/live-serial/', views.api_live_serial, name='api_live_serial'),
]