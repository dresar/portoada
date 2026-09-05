from django.contrib import admin
from .models import (
    Profile, About, Education, Skill, Project, Experience, 
    Certificate, Contact, Service, Testimonial, Blog, Award, 
    SocialMedia, PortfolioSettings
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'city', 'country', 'is_active', 'created_at']
    list_filter = ['is_active', 'city', 'country', 'created_at']
    search_fields = ['name', 'title', 'email', 'bio']
    list_editable = ['is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('name', 'title', 'bio', 'short_bio', 'email', 'phone')
        }),
        ('Alamat', {
            'fields': ('address', 'city', 'country')
        }),
        ('Informasi Pribadi', {
            'fields': ('birth_date', 'age')
        }),
        ('Media', {
            'fields': ('profile_image', 'cover_image', 'resume')
        }),
        ('Social Media', {
            'fields': ('website', 'github', 'linkedin', 'twitter', 'instagram'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['profile', 'story_title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['story_title', 'story_content', 'mission', 'vision']
    list_editable = ['is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['degree', 'is_current', 'is_active', 'start_date', 'end_date']
    search_fields = ['institution', 'field_of_study', 'description']
    list_editable = ['is_active', 'is_current']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'percentage', 'years_experience', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'percentage']
    search_fields = ['name', 'description']
    list_editable = ['percentage', 'is_featured', 'is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'end_date', 'is_featured', 'is_active']
    list_filter = ['status', 'is_featured', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'technologies']
    list_editable = ['is_featured', 'is_active', 'status']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company', 'employment_type', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['employment_type', 'is_current', 'is_active', 'start_date', 'end_date']
    search_fields = ['position', 'company', 'description']
    list_editable = ['is_active', 'is_current']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'issue_date', 'expiry_date', 'is_featured', 'is_active']
    list_filter = ['is_featured', 'is_active', 'issue_date', 'expiry_date']
    search_fields = ['title', 'issuer', 'description']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'issue_date'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    readonly_fields = ['id', 'ip_address', 'user_agent', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'price_range', 'delivery_time', 'is_active']
    list_filter = ['is_active', 'delivery_time']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_company', 'rating', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['client_name', 'client_company', 'testimonial']
    list_editable = ['rating', 'is_featured', 'is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'read_time', 'views', 'is_featured', 'is_active', 'published_at']
    list_filter = ['status', 'is_featured', 'is_active', 'published_at', 'created_at']
    search_fields = ['title', 'excerpt', 'content', 'tags']
    list_editable = ['status', 'is_featured', 'is_active']
    readonly_fields = ['id', 'views', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'category', 'date_received', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'date_received']
    search_fields = ['title', 'issuer', 'description']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'date_received'

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform', 'username', 'url', 'is_active']
    list_filter = ['platform', 'is_active']
    search_fields = ['username', 'url']
    list_editable = ['is_active']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(PortfolioSettings)
class PortfolioSettingsAdmin(admin.ModelAdmin):
    list_display = ['profile', 'site_title', 'theme_color', 'enable_animations']
    list_filter = ['enable_animations', 'enable_blog', 'enable_testimonials', 'enable_services', 'enable_awards']
    search_fields = ['site_title', 'site_description']
    readonly_fields = ['id', 'created_at', 'updated_at']
