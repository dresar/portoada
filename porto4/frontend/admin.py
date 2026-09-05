from django.contrib import admin
from .models import (
    UserProfile, SkillCategory, Skill, Education, Experience,
    ProjectCategory, Technology, Project, ProjectImage, Testimonial,
    Certificate, CertificateCategory, BlogCategory, BlogTag, BlogPost, BlogComment,
    Service, ContactMessage, SiteSettings, Award, Statistic
)

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('created_at', 'updated_at')

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'created_at')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current')
    search_fields = ('institution', 'degree', 'field_of_study')
    list_filter = ('is_current', 'start_date', 'end_date')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'start_date', 'end_date', 'is_current')
    search_fields = ('company', 'position')
    list_filter = ('is_current', 'start_date', 'end_date')

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name',)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date', 'end_date', 'is_featured')
    search_fields = ('title', 'description', 'short_description')
    list_filter = ('category', 'is_featured', 'start_date', 'end_date')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    filter_horizontal = ('technologies',)

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption', 'is_primary', 'created_at')
    search_fields = ('project__title', 'caption')
    list_filter = ('is_primary', 'created_at')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'rating', 'is_featured')
    search_fields = ('name', 'position', 'company', 'content')
    list_filter = ('rating', 'is_featured', 'created_at')

@admin.register(CertificateCategory)
class CertificateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'issuer', 'date_issued', 'is_featured')
    search_fields = ('title', 'issuer', 'credential_id')
    list_filter = ('category', 'issuer', 'date_issued', 'is_featured')

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ('name', 'email', 'website', 'content', 'created_at')
    can_delete = True
    show_change_link = True

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_date', 'views_count', 'is_featured')
    search_fields = ('title', 'content', 'excerpt')
    list_filter = ('status', 'category', 'is_featured', 'published_date')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    inlines = [BlogCommentInline]
    date_hierarchy = 'published_date'

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'email', 'is_approved', 'created_at')
    search_fields = ('name', 'email', 'content', 'post__title')
    list_filter = ('is_approved', 'created_at')
    readonly_fields = ('name', 'email', 'website', 'content', 'post', 'parent')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_featured', 'created_at')
    search_fields = ('title', 'short_description', 'description')
    list_filter = ('is_featured', 'created_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'email', 'phone', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_title', 'site_description', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'github', 'youtube')
        }),
        ('SEO Settings', {
            'fields': ('meta_keywords', 'meta_description', 'google_analytics_id')
        }),
    )

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'date_received', 'created_at')
    search_fields = ('title', 'organization', 'description')
    list_filter = ('date_received', 'created_at')

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'icon', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_featured', 'created_at')
