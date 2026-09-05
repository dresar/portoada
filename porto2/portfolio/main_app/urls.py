from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    # Halaman Utama - Single Page Application
    path('', views.home, name='home'),
    
    # Halaman Detail (untuk SEO dan sharing)
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Legacy URLs - redirect ke home (untuk backward compatibility)
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
]
    
  