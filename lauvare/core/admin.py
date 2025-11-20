from django.contrib import admin
from .models import Professional, Client


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('alias', 'plan', 'price_from', 'price_to', 'is_active')
    list_filter = ('plan', 'is_active')
    search_fields = ('alias', 'name', 'phone')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
