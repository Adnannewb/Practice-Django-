from django.contrib import admin
from .models import UserProfile,Registration,Event,Category
# Register your models here.

admin.site.register(Registration)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(UserProfile)
