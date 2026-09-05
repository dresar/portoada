from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.admin_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Personal Info management
    path('personal-info/', views.personal_info_edit, name='personal_info_edit'),
    
    # Social Media management
    path('social-media/', views.social_media_list, name='social_media_list'),
    path('social-media/add/', views.social_media_add, name='social_media_add'),
    path('social-media/edit/<int:pk>/', views.social_media_edit, name='social_media_edit'),
    path('social-media/delete/<int:pk>/', views.social_media_delete, name='social_media_delete'),
    
    # Project management
    path('projects/', views.project_list, name='project_list'),
    path('projects/add/', views.project_add, name='project_add'),
    path('projects/edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),
    
    # Project Category management
    path('project-categories/', views.project_category_list, name='project_category_list'),
    path('project-categories/add/', views.project_category_add, name='project_category_add'),
    path('project-categories/edit/<int:pk>/', views.project_category_edit, name='project_category_edit'),
    path('project-categories/delete/<int:pk>/', views.project_category_delete, name='project_category_delete'),
    
    # Project Image management
    path('projects/<int:project_id>/images/', views.project_image_list, name='project_image_list'),
    path('projects/<int:project_id>/images/add/', views.project_image_add, name='project_image_add'),
    path('projects/images/edit/<int:pk>/', views.project_image_edit, name='project_image_edit'),
    path('projects/images/delete/<int:pk>/', views.project_image_delete, name='project_image_delete'),
    
    # Skill Category management
    path('skill-categories/', views.skill_category_list, name='skill_category_list'),
    path('skill-categories/add/', views.skill_category_add, name='skill_category_add'),
    path('skill-categories/edit/<int:pk>/', views.skill_category_edit, name='skill_category_edit'),
    path('skill-categories/delete/<int:pk>/', views.skill_category_delete, name='skill_category_delete'),
    
    # Skills management
    path('skills/', views.skill_list, name='skill_list'),
    path('skills/add/', views.skill_add, name='skill_add'),
    path('skills/edit/<int:pk>/', views.skill_edit, name='skill_edit'),
    path('skills/delete/<int:pk>/', views.skill_delete, name='skill_delete'),
    
    # Education management
    path('education/', views.education_list, name='education_list'),
    path('education/add/', views.education_add, name='education_add'),
    path('education/edit/<int:pk>/', views.education_edit, name='education_edit'),
    path('education/delete/<int:pk>/', views.education_delete, name='education_delete'),
    
    # Experience management
    path('experience/', views.experience_list, name='experience_list'),
    path('experience/add/', views.experience_add, name='experience_add'),
    path('experience/edit/<int:pk>/', views.experience_edit, name='experience_edit'),
    path('experience/delete/<int:pk>/', views.experience_delete, name='experience_delete'),
    
    # Certificate management
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/add/', views.certificate_add, name='certificate_add'),
    path('certificates/edit/<int:pk>/', views.certificate_edit, name='certificate_edit'),
    path('certificates/delete/<int:pk>/', views.certificate_delete, name='certificate_delete'),
    
    # Service management
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_add, name='service_add'),
    path('services/edit/<int:pk>/', views.service_edit, name='service_edit'),
    path('services/delete/<int:pk>/', views.service_delete, name='service_delete'),
    
    # Testimonial management
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('testimonials/add/', views.testimonial_add, name='testimonial_add'),
    path('testimonials/edit/<int:pk>/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/delete/<int:pk>/', views.testimonial_delete, name='testimonial_delete'),
    
    # Contact Message management
    path('contact-messages/', views.contact_message_list, name='contact_message_list'),
    path('contact-messages/view/<int:pk>/', views.contact_message_view, name='contact_message_view'),
    path('contact-messages/delete/<int:pk>/', views.contact_message_delete, name='contact_message_delete'),
    
    # Blog Category management
    path('blog-categories/', views.blog_category_list, name='blog_category_list'),
    path('blog-categories/add/', views.blog_category_add, name='blog_category_add'),
    path('blog-categories/edit/<int:pk>/', views.blog_category_edit, name='blog_category_edit'),
    path('blog-categories/delete/<int:pk>/', views.blog_category_delete, name='blog_category_delete'),
    
    # Blog Post management
    path('blog-posts/', views.blog_post_list, name='blog_post_list'),
    path('blog-posts/add/', views.blog_post_add, name='blog_post_add'),
    path('blog-posts/edit/<int:pk>/', views.blog_post_edit, name='blog_post_edit'),
    path('blog-posts/delete/<int:pk>/', views.blog_post_delete, name='blog_post_delete'),
]