# contact_qr/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate_qr/', views.generate_qr_code, name='generate_qr'),
    path('download_qr/', views.download_qr_code, name='download_qr_code'),
]
