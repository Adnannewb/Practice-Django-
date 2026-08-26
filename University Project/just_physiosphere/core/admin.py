from django.contrib import admin
from .models import User, Therapist, Service, Appointment, Payment, MedicalCard, Visit, Message, AuditLog
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'role', 'is_student')}),
    )
    list_display = ('username', 'email', 'role', 'is_student', 'is_staff')

admin.site.register(Therapist)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(Payment)
admin.site.register(MedicalCard)
admin.site.register(Visit)
admin.site.register(Message)
admin.site.register(AuditLog)