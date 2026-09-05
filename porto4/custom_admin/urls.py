from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Authentication
    path('', views.admin_login, name='login'),
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User Management
    path('users/', views.UserManagementView.as_view(), name='users'),
    path('userprofiles/', views.UserProfileView.as_view(), name='userprofiles'),
    
    # Skills
    path('skill-categories/', views.SkillCategoryView.as_view(), name='skill_categories'),
    path('skills/', views.SkillView.as_view(), name='skills'),
    
    # Education & Experience
    path('education/', views.EducationView.as_view(), name='education'),
    path('experience/', views.ExperienceView.as_view(), name='experience'),
    
    # Projects
    path('project-categories/', views.ProjectCategoryView.as_view(), name='project_categories'),
    path('technologies/', views.TechnologyView.as_view(), name='technologies'),
    path('projects/', views.ProjectView.as_view(), name='projects'),
    
    # Certificates
    path('certificate-categories/', views.CertificateCategoryView.as_view(), name='certificate_categories'),
    path('certificates/', views.CertificateView.as_view(), name='certificates'),
    
    # Blog
    path('blog-categories/', views.BlogCategoryView.as_view(), name='blog_categories'),
    path('blog-tags/', views.BlogTagView.as_view(), name='blog_tags'),
    path('blog-posts/', views.BlogPostView.as_view(), name='blog_posts'),
    
    # Services & Others
    path('services/', views.ServiceView.as_view(), name='services'),
    path('contact-messages/', views.ContactMessageView.as_view(), name='contact_messages'),
    path('site-settings/', views.SiteSettingsView.as_view(), name='site_settings'),
    path('awards/', views.AwardView.as_view(), name='awards'),
    path('statistics/', views.StatisticView.as_view(), name='statistics'),
    path('testimonials/', views.TestimonialView.as_view(), name='testimonials'),
    
    # API endpoints
    path('api/get-object/<str:model_name>/<int:obj_id>/', views.get_object_data, name='get_object_data'),
    path('api/bulk-delete/', views.bulk_delete, name='bulk_delete'),
    path('api/export/<str:model_name>/', views.export_data, name='export_data'),
    path('api/upload/', views.upload_file, name='upload_file'),
    path('api/search/', views.global_search, name='global_search'),
]