from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # Halaman Utama
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
] 