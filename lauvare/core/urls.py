from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('profesional/<int:pk>/', views.professional_detail, name='professional_detail'),
    path('pricing/', views.pricing, name='pricing'),
    path('api/professionals/', views.professionals_api, name='professionals_api'),
]
