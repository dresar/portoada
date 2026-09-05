from django.urls import path
from . import views
from . import auth

app_name = 'portfolio_admin'

urlpatterns = [
    # Authentication
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Profile URLs
    path('profile/', views.profile_list, name='profile_list'),
    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/<int:pk>/update/', views.profile_update, name='profile_update'),
    path('profile/<int:pk>/delete/', views.profile_delete, name='profile_delete'),
    
    # About URLs
    path('about/', views.about_list, name='about_list'),
    path('about/create/', views.about_create, name='about_create'),
    path('about/<int:pk>/update/', views.about_update, name='about_update'),
    path('about/<int:pk>/delete/', views.about_delete, name='about_delete'),
    
    # Education URLs
    path('education/', views.education_list, name='education_list'),
    path('education/create/', views.education_create, name='education_create'),
    path('education/<int:pk>/update/', views.education_update, name='education_update'),
    path('education/<int:pk>/delete/', views.education_delete, name='education_delete'),
    
    # Skill URLs
    path('skill/', views.skill_list, name='skill_list'),
    path('skill/create/', views.skill_create, name='skill_create'),
    path('skill/<int:pk>/update/', views.skill_update, name='skill_update'),
    path('skill/<int:pk>/delete/', views.skill_delete, name='skill_delete'),
    
    # Project URLs
    path('project/', views.project_list, name='project_list'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/update/', views.project_update, name='project_update'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Experience URLs
    path('experience/', views.experience_list, name='experience_list'),
    path('experience/create/', views.experience_create, name='experience_create'),
    path('experience/<int:pk>/update/', views.experience_update, name='experience_update'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
    
    # Certificate URLs
    path('certificate/', views.certificate_list, name='certificate_list'),
    path('certificate/create/', views.certificate_create, name='certificate_create'),
    path('certificate/<int:pk>/update/', views.certificate_update, name='certificate_update'),
    path('certificate/<int:pk>/delete/', views.certificate_delete, name='certificate_delete'),
    
    # Contact URLs
    path('contact/', views.contact_list, name='contact_list'),
    path('contact/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contact/<int:pk>/delete/', views.contact_delete, name='contact_delete'),
    
    # Service URLs
    path('service/', views.service_list, name='service_list'),
    path('service/create/', views.service_create, name='service_create'),
    path('service/<int:pk>/update/', views.service_update, name='service_update'),
    path('service/<int:pk>/delete/', views.service_delete, name='service_delete'),
    
    # Testimonial URLs
    path('testimonial/', views.testimonial_list, name='testimonial_list'),
    path('testimonial/create/', views.testimonial_create, name='testimonial_create'),
    path('testimonial/<int:pk>/update/', views.testimonial_update, name='testimonial_update'),
    path('testimonial/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),
    
    # Blog Category URLs
    path('blog-category/', views.blog_category_list, name='blog_category_list'),
    path('blog-category/create/', views.blog_category_create, name='blog_category_create'),
    path('blog-category/<int:pk>/update/', views.blog_category_update, name='blog_category_update'),
    path('blog-category/<int:pk>/delete/', views.blog_category_delete, name='blog_category_delete'),
    
    # Blog Tag URLs
    path('blog-tag/', views.blog_tag_list, name='blog_tag_list'),
    path('blog-tag/create/', views.blog_tag_create, name='blog_tag_create'),
    path('blog-tag/<int:pk>/update/', views.blog_tag_update, name='blog_tag_update'),
    path('blog-tag/<int:pk>/delete/', views.blog_tag_delete, name='blog_tag_delete'),
    
    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/update/', views.blog_update, name='blog_update'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    
    # Blog Comment URLs
    path('blog-comment/', views.blog_comment_list, name='blog_comment_list'),
    path('blog-comment/<int:pk>/', views.blog_comment_detail, name='blog_comment_detail'),
    path('blog-comment/<int:pk>/approve/', views.blog_comment_approve, name='blog_comment_approve'),
    path('blog-comment/<int:pk>/delete/', views.blog_comment_delete, name='blog_comment_delete'),
    
    # Award URLs
    path('award/', views.award_list, name='award_list'),
    path('award/create/', views.award_create, name='award_create'),
    path('award/<int:pk>/update/', views.award_update, name='award_update'),
    path('award/<int:pk>/delete/', views.award_delete, name='award_delete'),
    
    # Social Media URLs
    path('social-media/', views.social_media_list, name='social_media_list'),
    path('social-media/create/', views.social_media_create, name='social_media_create'),
    path('social-media/<int:pk>/update/', views.social_media_update, name='social_media_update'),
    path('social-media/<int:pk>/delete/', views.social_media_delete, name='social_media_delete'),
    
    # Portfolio Settings URLs
    path('settings/', views.portfolio_settings, name='portfolio_settings'),
    # path('settings/update/', views.portfolio_settings_update, name='portfolio_settings_update'),
    
    # Preview URLs
    path('preview/profile/', views.profile_preview, name='profile_preview'),
    path('preview/about/', views.about_preview, name='about_preview'),
    path('preview/education/', views.education_preview, name='education_preview'),
    path('preview/skill/', views.skill_preview, name='skill_preview'),
    path('preview/project/', views.project_preview, name='project_preview'),
    path('preview/experience/', views.experience_preview, name='experience_preview'),
    path('preview/certificate/', views.certificate_preview, name='certificate_preview'),
    path('preview/service/', views.service_preview, name='service_preview'),
    path('preview/testimonial/', views.testimonial_preview, name='testimonial_preview'),
    path('preview/blog/', views.blog_preview, name='blog_preview'),
    path('preview/award/', views.award_preview, name='award_preview'),
    path('preview/contact/', views.contact_preview, name='contact_preview'),
]