from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    # Skill URLs
    path('skills/', views.skill_list, name='skill_list'),
    path('skills/modal/create/', views.skill_modal_create, name='skill_modal_create'),
    path('skills/modal/edit/<int:pk>/', views.skill_modal_edit, name='skill_modal_edit'),
    path('skills/ajax/create/', views.skill_ajax_create, name='skill_ajax_create'),
    path('skills/ajax/update/<int:skill_id>/', views.skill_ajax_update, name='skill_ajax_update'),
    path('skills/ajax/delete/<int:skill_id>/', views.skill_ajax_delete, name='skill_ajax_delete'),
    path('skills/toggle-status/<int:skill_id>/', views.skill_toggle_status, name='skill_toggle_status'),
    path('skills/toggle-featured/<int:skill_id>/', views.skill_toggle_featured, name='skill_toggle_featured'),
    
    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('projects/modal/create/', views.project_modal_create, name='project_modal_create'),
    path('projects/modal/edit/<int:pk>/', views.project_modal_edit, name='project_modal_edit'),
    path('projects/ajax/create/', views.project_ajax_create, name='project_ajax_create'),
    path('projects/ajax/update/<int:project_id>/', views.project_ajax_update, name='project_ajax_update'),
    path('projects/ajax/delete/<int:project_id>/', views.project_ajax_delete, name='project_ajax_delete'),
    path('projects/toggle-status/<int:project_id>/', views.project_toggle_status, name='project_toggle_status'),
    path('projects/toggle-featured/<int:project_id>/', views.project_toggle_featured, name='project_toggle_featured'),
    
    # Experience URLs
    path('experience/', views.experience_list, name='experience_list'),
    path('experience/modal/create/', views.experience_modal_create, name='experience_modal_create'),
    path('experience/modal/edit/<int:pk>/', views.experience_modal_edit, name='experience_modal_edit'),
    path('experience/ajax/create/', views.experience_ajax_create, name='experience_ajax_create'),
    path('experience/ajax/update/<int:experience_id>/', views.experience_ajax_update, name='experience_ajax_update'),
    path('experience/ajax/delete/<int:experience_id>/', views.experience_ajax_delete, name='experience_ajax_delete'),
    path('experience/toggle-status/<int:experience_id>/', views.experience_toggle_status, name='experience_toggle_status'),
    path('experience/toggle-current/<int:experience_id>/', views.experience_toggle_current, name='experience_toggle_current'),
    
    # Certificate URLs
    path('certificates/', views.certificate_list, name='certificate_list'),
    path('certificates/detail/<int:pk>/', views.certificate_detail, name='certificate_detail'),
    path('certificates/modal/create/', views.certificate_modal_create, name='certificate_modal_create'),
    path('certificates/modal/edit/<int:pk>/', views.certificate_modal_edit, name='certificate_modal_edit'),
    path('certificates/ajax/create/', views.certificate_ajax_create, name='certificate_ajax_create'),
    path('certificates/ajax/update/<int:certificate_id>/', views.certificate_ajax_update, name='certificate_ajax_update'),
    path('certificates/ajax/delete/<int:certificate_id>/', views.certificate_ajax_delete, name='certificate_ajax_delete'),
    path('certificates/toggle-status/<int:certificate_id>/', views.certificate_toggle_status, name='certificate_toggle_status'),
    
    # Education URLs
    path('education/', views.education_list, name='education_list'),
    path('education/modal/create/', views.education_modal_create, name='education_modal_create'),
    path('education/modal/edit/<int:pk>/', views.education_modal_edit, name='education_modal_edit'),
    path('education/ajax/create/', views.education_ajax_create, name='education_ajax_create'),
    path('education/ajax/update/<int:education_id>/', views.education_ajax_update, name='education_ajax_update'),
    path('education/ajax/delete/<int:education_id>/', views.education_ajax_delete, name='education_ajax_delete'),
    path('education/toggle-status/<int:education_id>/', views.education_toggle_status, name='education_toggle_status'),
    
    # Award URLs
    path('awards/', views.award_list, name='award_list'),
    path('awards/modal/create/', views.award_modal_create, name='award_modal_create'),
    path('awards/modal/edit/<int:pk>/', views.award_modal_edit, name='award_modal_edit'),
    path('awards/ajax/create/', views.award_ajax_create, name='award_ajax_create'),
    path('awards/ajax/update/<int:award_id>/', views.award_ajax_update, name='award_ajax_update'),
    path('awards/ajax/delete/<int:award_id>/', views.award_ajax_delete, name='award_ajax_delete'),
    path('awards/toggle-status/<int:award_id>/', views.award_toggle_status, name='award_toggle_status'),
    path('awards/toggle-featured/<int:award_id>/', views.award_toggle_featured, name='award_toggle_featured'),
    
    # Service URLs
    path('services/', views.service_list, name='service_list'),
    path('services/modal/create/', views.service_modal_create, name='service_modal_create'),
    path('services/modal/edit/<int:pk>/', views.service_modal_edit, name='service_modal_edit'),
    path('services/ajax/create/', views.service_ajax_create, name='service_ajax_create'),
    path('services/ajax/update/<int:service_id>/', views.service_ajax_update, name='service_ajax_update'),
    path('services/ajax/delete/<int:service_id>/', views.service_ajax_delete, name='service_ajax_delete'),
    path('services/toggle-status/<int:service_id>/', views.service_toggle_status, name='service_toggle_status'),
    path('services/toggle-featured/<int:service_id>/', views.service_toggle_featured, name='service_toggle_featured'),
    
    # Testimonial URLs
    path('testimonials/', views.testimonial_list, name='testimonial_list'),
    path('testimonials/modal/create/', views.testimonial_modal_create, name='testimonial_modal_create'),
    path('testimonials/modal/edit/<int:pk>/', views.testimonial_modal_edit, name='testimonial_modal_edit'),
    path('testimonials/ajax/create/', views.testimonial_ajax_create, name='testimonial_ajax_create'),
    path('testimonials/ajax/update/<int:testimonial_id>/', views.testimonial_ajax_update, name='testimonial_ajax_update'),
    path('testimonials/ajax/delete/<int:testimonial_id>/', views.testimonial_ajax_delete, name='testimonial_ajax_delete'),
    path('testimonials/toggle-status/<int:testimonial_id>/', views.testimonial_toggle_status, name='testimonial_toggle_status'),
    path('testimonials/toggle-featured/<int:testimonial_id>/', views.testimonial_toggle_featured, name='testimonial_toggle_featured'),
    
    # Contact URLs
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/detail/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contacts/ajax/delete/<int:contact_id>/', views.contact_ajax_delete, name='contact_ajax_delete'),
    path('contacts/mark-as-read/<int:contact_id>/', views.contact_mark_as_read, name='contact_mark_as_read'),
    path('contacts/mark-as-unread/<int:contact_id>/', views.contact_mark_as_unread, name='contact_mark_as_unread'),
    
    # About URLs
    path('about/', views.about_list, name='about_list'),
    path('about/detail/<int:pk>/', views.about_detail, name='about_detail'),
    path('about/modal/create/', views.about_modal_create, name='about_modal_create'),
    path('about/modal/edit/<int:pk>/', views.about_modal_edit, name='about_modal_edit'),
    path('about/ajax/create/', views.about_ajax_create, name='about_ajax_create'),
    path('about/ajax/update/<int:about_id>/', views.about_ajax_update, name='about_ajax_update'),
    path('about/ajax/delete/<int:about_id>/', views.about_ajax_delete, name='about_ajax_delete'),
    path('about/toggle-status/<int:about_id>/', views.about_toggle_status, name='about_toggle_status'),
    
    # Profile URLs
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/detail/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profiles/modal/create/', views.profile_modal_create, name='profile_modal_create'),
    path('profiles/modal/edit/<int:pk>/', views.profile_modal_edit, name='profile_modal_edit'),
    path('profiles/ajax/create/', views.profile_ajax_create, name='profile_ajax_create'),
    path('profiles/ajax/update/<int:profile_id>/', views.profile_ajax_update, name='profile_ajax_update'),
    path('profiles/ajax/delete/<int:profile_id>/', views.profile_ajax_delete, name='profile_ajax_delete'),
    path('profiles/toggle-status/<int:profile_id>/', views.profile_toggle_status, name='profile_toggle_status'),
]