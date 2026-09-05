from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from datetime import datetime

from frontend.models import (
    UserProfile, SkillCategory, Skill, Education, Experience,
    ProjectCategory, Technology, Project, ProjectImage, Testimonial,
    Certificate, CertificateCategory, BlogCategory, BlogTag, BlogPost, BlogComment,
    Service, ContactMessage, SiteSettings, Award, Statistic
)
from django.contrib.auth.models import User

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions')
    return render(request, 'custom_admin/login.html')

@login_required
@user_passes_test(is_admin)
def admin_logout(request):
    logout(request)
    return redirect('custom_admin:login')

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    stats = {
        'users': User.objects.count(),
        'projects': Project.objects.count(),
        'blog_posts': BlogPost.objects.count(),
        'messages': ContactMessage.objects.count(),
        'skills': Skill.objects.count(),
        'certificates': Certificate.objects.count(),
    }
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    recent_posts = BlogPost.objects.order_by('-created_at')[:5]
    return render(request, 'custom_admin/dashboard.html', {
        'stats': stats,
        'recent_messages': recent_messages,
        'recent_posts': recent_posts
    })

# Generic CRUD Views
class AdminCRUDView(View):
    model = None
    template_name = None
    fields = []
    search_fields = []
    
    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_admin))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        search = request.GET.get('search', '')
        objects = self.model.objects.all().order_by('-id')
        
        if search and self.search_fields:
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f'{field}__icontains': search})
            objects = objects.filter(query)
        
        paginator = Paginator(objects, 20)
        page = request.GET.get('page')
        objects = paginator.get_page(page)
        
        return render(request, self.template_name, {
            'objects': objects,
            'model_name': self.model._meta.verbose_name,
            'model_name_plural': self.model._meta.verbose_name_plural,
            'fields': self.fields,
            'search': search
        })
    
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'create':
            return self.create_object(request)
        elif action == 'update':
            return self.update_object(request)
        elif action == 'delete':
            return self.delete_object(request)
        
        return JsonResponse({'success': False, 'error': 'Invalid action'})
    
    def create_object(self, request):
        try:
            data = {}
            for field in self.fields:
                value = request.POST.get(field)
                if value:
                    data[field] = value
            
            obj = self.model.objects.create(**data)
            return JsonResponse({
                'success': True,
                'message': f'{self.model._meta.verbose_name} created successfully',
                'id': obj.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    def update_object(self, request):
        try:
            obj_id = request.POST.get('id')
            obj = get_object_or_404(self.model, id=obj_id)
            
            for field in self.fields:
                value = request.POST.get(field)
                if value is not None:
                    setattr(obj, field, value)
            
            obj.save()
            return JsonResponse({
                'success': True,
                'message': f'{self.model._meta.verbose_name} updated successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    def delete_object(self, request):
        try:
            obj_id = request.POST.get('id')
            obj = get_object_or_404(self.model, id=obj_id)
            obj.delete()
            return JsonResponse({
                'success': True,
                'message': f'{self.model._meta.verbose_name} deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

# User Management
class UserManagementView(AdminCRUDView):
    model = User
    template_name = 'custom_admin/users.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']

# UserProfile Management
class UserProfileView(AdminCRUDView):
    model = UserProfile
    template_name = 'custom_admin/userprofiles.html'
    fields = ['bio', 'phone', 'address', 'website', 'linkedin', 'github']
    search_fields = ['user__username', 'phone']

# Skill Category Management
class SkillCategoryView(AdminCRUDView):
    model = SkillCategory
    template_name = 'custom_admin/skill_categories.html'
    fields = ['name', 'icon', 'description']
    search_fields = ['name']

# Skill Management
class SkillView(AdminCRUDView):
    model = Skill
    template_name = 'custom_admin/skills.html'
    fields = ['name', 'category', 'proficiency', 'icon', 'description']
    search_fields = ['name', 'category__name']

# Education Management
class EducationView(AdminCRUDView):
    model = Education
    template_name = 'custom_admin/education.html'
    fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current', 'description']
    search_fields = ['institution', 'degree', 'field_of_study']

# Experience Management
class ExperienceView(AdminCRUDView):
    model = Experience
    template_name = 'custom_admin/experience.html'
    fields = ['company', 'position', 'start_date', 'end_date', 'is_current', 'description']
    search_fields = ['company', 'position']

# Project Category Management
class ProjectCategoryView(AdminCRUDView):
    model = ProjectCategory
    template_name = 'custom_admin/project_categories.html'
    fields = ['name', 'description']
    search_fields = ['name']

# Technology Management
class TechnologyView(AdminCRUDView):
    model = Technology
    template_name = 'custom_admin/technologies.html'
    fields = ['name', 'icon', 'description']
    search_fields = ['name']

# Project Management
class ProjectView(AdminCRUDView):
    model = Project
    template_name = 'custom_admin/projects.html'
    fields = ['title', 'slug', 'category', 'short_description', 'description', 'start_date', 'end_date', 'is_featured', 'github_url', 'live_url']
    search_fields = ['title', 'description', 'short_description']

# Certificate Category Management
class CertificateCategoryView(AdminCRUDView):
    model = CertificateCategory
    template_name = 'custom_admin/certificate_categories.html'
    fields = ['name', 'description']
    search_fields = ['name']

# Certificate Management
class CertificateView(AdminCRUDView):
    model = Certificate
    template_name = 'custom_admin/certificates.html'
    fields = ['title', 'category', 'issuer', 'date_issued', 'expiry_date', 'credential_id', 'credential_url', 'description', 'is_featured']
    search_fields = ['title', 'issuer', 'credential_id']

# Blog Category Management
class BlogCategoryView(AdminCRUDView):
    model = BlogCategory
    template_name = 'custom_admin/blog_categories.html'
    fields = ['name', 'slug', 'description']
    search_fields = ['name']

# Blog Tag Management
class BlogTagView(AdminCRUDView):
    model = BlogTag
    template_name = 'custom_admin/blog_tags.html'
    fields = ['name', 'slug']
    search_fields = ['name']

# Blog Post Management
class BlogPostView(AdminCRUDView):
    model = BlogPost
    template_name = 'custom_admin/blog_posts.html'
    fields = ['title', 'slug', 'author', 'content', 'excerpt', 'category', 'status', 'is_featured', 'published_date']
    search_fields = ['title', 'content', 'excerpt']

# Service Management
class ServiceView(AdminCRUDView):
    model = Service
    template_name = 'custom_admin/services.html'
    fields = ['title', 'icon', 'short_description', 'description', 'is_featured']
    search_fields = ['title', 'short_description']

# Contact Message Management
class ContactMessageView(AdminCRUDView):
    model = ContactMessage
    template_name = 'custom_admin/contact_messages.html'
    fields = ['name', 'email', 'subject', 'message', 'is_read']
    search_fields = ['name', 'email', 'subject']

# Site Settings Management
class SiteSettingsView(AdminCRUDView):
    model = SiteSettings
    template_name = 'custom_admin/site_settings.html'
    fields = ['site_title', 'site_description', 'email', 'phone', 'address', 'facebook', 'twitter', 'instagram', 'linkedin', 'github', 'youtube']
    search_fields = ['site_title']

# Award Management
class AwardView(AdminCRUDView):
    model = Award
    template_name = 'custom_admin/awards.html'
    fields = ['title', 'organization', 'date_received', 'description']
    search_fields = ['title', 'organization']

# Statistic Management
class StatisticView(AdminCRUDView):
    model = Statistic
    template_name = 'custom_admin/statistics.html'
    fields = ['title', 'value', 'icon', 'description', 'is_featured']
    search_fields = ['title']

# Testimonial Management
class TestimonialView(AdminCRUDView):
    model = Testimonial
    template_name = 'custom_admin/testimonials.html'
    fields = ['name', 'position', 'company', 'content', 'rating', 'is_featured']
    search_fields = ['name', 'position', 'company']

# API Views for AJAX operations
@csrf_exempt
@login_required
@user_passes_test(is_admin)
def get_object_data(request, model_name, obj_id):
    """Get object data for editing"""
    model_map = {
        'user': User,
        'userprofile': UserProfile,
        'skillcategory': SkillCategory,
        'skill': Skill,
        'education': Education,
        'experience': Experience,
        'projectcategory': ProjectCategory,
        'technology': Technology,
        'project': Project,
        'certificatecategory': CertificateCategory,
        'certificate': Certificate,
        'blogcategory': BlogCategory,
        'blogtag': BlogTag,
        'blogpost': BlogPost,
        'service': Service,
        'contactmessage': ContactMessage,
        'sitesettings': SiteSettings,
        'award': Award,
        'statistic': Statistic,
        'testimonial': Testimonial,
    }
    
    model = model_map.get(model_name.lower())
    if not model:
        return JsonResponse({'success': False, 'error': 'Model not found'})
    
    try:
        obj = get_object_or_404(model, id=obj_id)
        data = {}
        
        for field in obj._meta.fields:
            value = getattr(obj, field.name)
            if hasattr(value, 'isoformat'):  # datetime objects
                data[field.name] = value.isoformat()
            elif hasattr(value, 'id'):  # foreign key objects
                data[field.name] = value.id
            else:
                data[field.name] = value
        
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@login_required
@user_passes_test(is_admin)
def bulk_delete(request):
    """Bulk delete objects"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            model_name = data.get('model')
            ids = data.get('ids', [])
            
            model_map = {
                'user': User,
                'userprofile': UserProfile,
                'skillcategory': SkillCategory,
                'skill': Skill,
                'education': Education,
                'experience': Experience,
                'projectcategory': ProjectCategory,
                'technology': Technology,
                'project': Project,
                'certificatecategory': CertificateCategory,
                'certificate': Certificate,
                'blogcategory': BlogCategory,
                'blogtag': BlogTag,
                'blogpost': BlogPost,
                'service': Service,
                'contactmessage': ContactMessage,
                'sitesettings': SiteSettings,
                'award': Award,
                'statistic': Statistic,
                'testimonial': Testimonial,
            }
            
            model = model_map.get(model_name.lower())
            if not model:
                return JsonResponse({'success': False, 'error': 'Model not found'})
            
            deleted_count = model.objects.filter(id__in=ids).delete()[0]
            return JsonResponse({
                'success': True,
                'message': f'{deleted_count} items deleted successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@user_passes_test(is_admin)
def export_data(request, model_name):
    """Export data to CSV"""
    import csv
    from django.http import HttpResponse
    
    model_map = {
        'user': User,
        'userprofile': UserProfile,
        'skillcategory': SkillCategory,
        'skill': Skill,
        'education': Education,
        'experience': Experience,
        'projectcategory': ProjectCategory,
        'technology': Technology,
        'project': Project,
        'certificatecategory': CertificateCategory,
        'certificate': Certificate,
        'blogcategory': BlogCategory,
        'blogtag': BlogTag,
        'blogpost': BlogPost,
        'service': Service,
        'contactmessage': ContactMessage,
        'sitesettings': SiteSettings,
        'award': Award,
        'statistic': Statistic,
        'testimonial': Testimonial,
    }
    
    model = model_map.get(model_name.lower())
    if not model:
        return JsonResponse({'success': False, 'error': 'Model not found'})
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'
    
    writer = csv.writer(response)
    
    # Write header
    field_names = [field.name for field in model._meta.fields]
    writer.writerow(field_names)
    
    # Write data
    for obj in model.objects.all():
        row = []
        for field_name in field_names:
            value = getattr(obj, field_name)
            if hasattr(value, 'isoformat'):  # datetime objects
                row.append(value.isoformat())
            elif hasattr(value, 'id'):  # foreign key objects
                row.append(str(value))
            else:
                row.append(str(value) if value is not None else '')
        writer.writerow(row)
    
    return response

# File upload handler
@csrf_exempt
@login_required
@user_passes_test(is_admin)
def upload_file(request):
    """Handle file uploads"""
    if request.method == 'POST' and request.FILES:
        try:
            uploaded_file = request.FILES['file']
            # Handle file upload logic here
            # For now, just return success
            return JsonResponse({
                'success': True,
                'message': 'File uploaded successfully',
                'filename': uploaded_file.name
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'No file uploaded'})

# Search functionality
@login_required
@user_passes_test(is_admin)
def global_search(request):
    """Global search across all models"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Search in different models
        models_to_search = [
            (User, ['username', 'email', 'first_name', 'last_name']),
            (Project, ['title', 'description', 'short_description']),
            (BlogPost, ['title', 'content', 'excerpt']),
            (Skill, ['name']),
            (Service, ['title', 'description']),
        ]
        
        for model, fields in models_to_search:
            search_query = Q()
            for field in fields:
                search_query |= Q(**{f'{field}__icontains': query})
            
            objects = model.objects.filter(search_query)[:5]
            for obj in objects:
                results.append({
                    'model': model._meta.verbose_name,
                    'title': str(obj),
                    'url': f'/custom-admin/{model._meta.model_name}/',
                    'id': obj.id
                })
    
    return JsonResponse({'results': results})
