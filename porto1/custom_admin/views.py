from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
import json
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout

from .models import (
    Profile, About, Education, Skill, Project, Experience, 
    Certificate, Contact, Service, Testimonial, Blog, Award,
    BlogCategory, BlogTag, BlogComment, SocialMedia, PortfolioSettings
)
from .utils import handle_file_upload, delete_file_if_exists

# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def login_view(request):
    """
    Login view for custom admin
    """
    if request.user.is_authenticated:
        return redirect('custom_admin:dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'custom_admin:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'custom_admin/auth/login.html')

@login_required
def logout_view(request):
    """
    Logout view for custom admin
    """
    logout(request)
    return redirect('custom_admin:login')

# ============================================================================
# DASHBOARD VIEW
# ============================================================================

@login_required
def dashboard(request):
    """
    Dashboard view showing statistics and recent activities
    """
    # Get counts for statistics
    project_count = Project.objects.count()
    skill_count = Skill.objects.count()
    experience_count = Experience.objects.count()
    unread_contact_count = Contact.objects.filter(status='new').count()
    
    # Get recent projects
    recent_projects = Project.objects.order_by('-created_at')[:5]
    
    # Get recent messages
    recent_messages = Contact.objects.order_by('-created_at')[:5]
    
    context = {
        'project_count': project_count,
        'skill_count': skill_count,
        'experience_count': experience_count,
        'unread_contact_count': unread_contact_count,
        'recent_projects': recent_projects,
        'recent_messages': recent_messages,
    }
    
    return render(request, 'custom_admin/dashboard.html', context)

# ============================================================================
# GENERIC CRUD VIEWS
# ============================================================================

def generic_list_view(request, model, template, context_name, per_page=10, **extra_context):
    """
    Generic list view for any model with pagination and search
    """
    search_query = request.GET.get('search', '')
    objects = model.objects.all()
    
    # Apply search if provided
    if search_query:
        # This is a basic search - customize the Q objects based on your model's searchable fields
        search_fields = extra_context.get('search_fields', [])
        if search_fields:
            q_objects = Q()
            for field in search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_query})
            objects = objects.filter(q_objects)
    
    # Apply any additional filters from the request
    filter_fields = extra_context.get('filter_fields', {})
    for field, param in filter_fields.items():
        value = request.GET.get(param)
        if value:
            objects = objects.filter(**{field: value})
    
    # Apply ordering
    order_by = request.GET.get('order_by', extra_context.get('default_order', '-id'))
    objects = objects.order_by(order_by)
    
    # Pagination
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Prepare context
    context = {
        context_name: page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': objects.count(),
    }
    
    # Add any extra context
    context.update(extra_context)
    
    return render_to_string(template, context, request=request)

@login_required
@require_POST
def generic_toggle_status(request, model, pk):
    """
    Generic view to toggle the is_active status of any model
    """
    obj = get_object_or_404(model, pk=pk)
    obj.is_active = not obj.is_active
    obj.save()
    
    return JsonResponse({
        'success': True,
        'is_active': obj.is_active
    })

@login_required
@require_POST
def generic_toggle_featured(request, model, pk):
    """
    Generic view to toggle the is_featured status of any model
    """
    obj = get_object_or_404(model, pk=pk)
    obj.is_featured = not obj.is_featured
    obj.save()
    
    return JsonResponse({
        'success': True,
        'is_featured': obj.is_featured
    })

@login_required
@require_POST
def generic_delete(request, model, pk):
    """
    Generic view to delete an instance of any model
    """
    obj = get_object_or_404(model, pk=pk)
    obj_name = str(obj)
    obj.delete()
    
    return JsonResponse({
        'success': True,
        'message': f"{model.__name__} '{obj_name}' deleted successfully"
    })

# ============================================================================
# MODAL VIEWS
# ============================================================================

@login_required
@require_POST
def render_modal_template(request, entity, modal_type):
    """
    Render a modal template for a specific entity and modal type
    """
    try:
        data = json.loads(request.body) if request.body else {}
        context = {'entity': entity, 'data': data}
        
        # Add entity-specific context
        if entity == 'skill':
            context['categories'] = Skill.CATEGORY_CHOICES
        elif entity == 'project':
            context['skills'] = Skill.objects.filter(is_active=True)
        elif entity == 'blog':
            context['categories'] = BlogCategory.objects.all()
            context['tags'] = BlogTag.objects.all()
        
        template_name = f'custom_admin/{entity}s/modal_{modal_type}.html'
        html = render_to_string(template_name, context, request)
        return HttpResponse(html)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# ============================================================================
# SKILL VIEWS
# ============================================================================

@login_required
def skill_list(request):
    """List all skills"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        category_filter = request.GET.get('category', '')
        
        skills = Skill.objects.all().order_by('category', 'name')
        
        if search_query:
            skills = skills.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                skills = skills.filter(is_active=True)
            elif status_filter == 'inactive':
                skills = skills.filter(is_active=False)
        
        if profile_filter:
            skills = skills.filter(profile_id=profile_filter)
            
        if category_filter:
            skills = skills.filter(category=category_filter)
        
        # Pagination
        paginator = Paginator(skills, 10)  # Show 10 skills per page
        page_number = request.GET.get('page')
        skills_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'skills_list': skills_list,
            'profiles': profiles,
            'categories': Skill.CATEGORY_CHOICES,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'category_filter': category_filter,
            'page_title': 'Skill Management',
            'active_menu': 'skills'
        }
        
        return render(request, 'custom_admin/skills/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading skills: {str(e)}')
        return render(request, 'custom_admin/skills/list.html', {'error': str(e)})

@login_required
def skill_modal_create(request):
    """
    Render the create skill modal form fields
    """
    context = {
        'categories': Skill.CATEGORY_CHOICES,
        'profiles': Profile.objects.filter(is_active=True)
    }
    return render(request, 'custom_admin/skills/modal_form_fields.html', context)

@login_required
def skill_modal_edit(request, pk):
    """
    Render the edit skill modal form fields
    """
    try:
        skill = Skill.objects.get(pk=pk)
        context = {
            'skill': skill,
            'categories': Skill.CATEGORY_CHOICES,
            'profiles': Profile.objects.filter(is_active=True)
        }
        return render(request, 'custom_admin/skills/modal_form_fields.html', context)
    except Skill.DoesNotExist:
        return JsonResponse({'error': 'Skill not found'}, status=404)

@login_required
@csrf_exempt
def skill_ajax_create(request):
    """AJAX create skill"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'category', 'percentage', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Create skill
            skill = Skill.objects.create(
                profile=profile,
                name=data['name'],
                category=data['category'],
                percentage=data['percentage'],
                description=data.get('description', ''),
                icon=data.get('icon', ''),
                color=data.get('color', '#3B82F6'),
                years_experience=data.get('years_experience', 0),
                is_featured=data.get('is_featured', False),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Skill created successfully!',
                'skill_id': str(skill.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def skill_ajax_update(request, skill_id):
    """AJAX update skill"""
    if request.method == 'POST':
        try:
            skill = get_object_or_404(Skill, id=skill_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'category', 'percentage', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Update skill
            skill.profile = profile
            skill.name = data['name']
            skill.category = data['category']
            skill.percentage = data['percentage']
            skill.description = data.get('description', '')
            skill.icon = data.get('icon', '')
            skill.color = data.get('color', '#3B82F6')
            skill.years_experience = data.get('years_experience', 0)
            skill.is_featured = data.get('is_featured', False)
            skill.is_active = data.get('is_active', True)
            skill.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Skill updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def skill_ajax_delete(request, skill_id):
    """AJAX delete skill"""
    if request.method == 'POST':
        try:
            skill = get_object_or_404(Skill, id=skill_id)
            skill.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Skill deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def skill_toggle_status(request, skill_id):
    """Toggle skill status"""
    try:
        skill = get_object_or_404(Skill, id=skill_id)
        skill.is_active = not skill.is_active
        skill.save()
        
        status = 'activated' if skill.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Skill {status} successfully!',
            'is_active': skill.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# PROJECT VIEWS
# ============================================================================

@login_required
def project_list(request):
    """List all projects"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        
        projects = Project.objects.all().order_by('-created_at')
        
        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(technologies__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                projects = projects.filter(is_active=True)
            elif status_filter == 'inactive':
                projects = projects.filter(is_active=False)
            elif status_filter in ['completed', 'ongoing', 'planned']:
                projects = projects.filter(status=status_filter)
        
        if profile_filter:
            projects = projects.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(projects, 10)  # Show 10 projects per page
        page_number = request.GET.get('page')
        projects_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'projects_list': projects_list,
            'profiles': profiles,
            'status_choices': Project.STATUS_CHOICES,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'page_title': 'Project Management',
            'active_menu': 'projects'
        }
        
        return render(request, 'custom_admin/projects/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading projects: {str(e)}')
        return render(request, 'custom_admin/projects/list.html', {'error': str(e)})

@login_required
def project_modal_create(request):
    """
    Render the create project modal form fields
    """
    context = {
        'skills': Skill.objects.filter(is_active=True),
        'profiles': Profile.objects.filter(is_active=True),
        'status_choices': Project.STATUS_CHOICES
    }
    return render(request, 'custom_admin/projects/modal_form_fields.html', context)

@login_required
def project_modal_edit(request, pk):
    """
    Render the edit project modal form fields
    """
    try:
        project = Project.objects.get(pk=pk)
        context = {
            'project': project,
            'skills': Skill.objects.filter(is_active=True),
            'profiles': Profile.objects.filter(is_active=True),
            'status_choices': Project.STATUS_CHOICES
        }
        return render(request, 'custom_admin/projects/modal_form_fields.html', context)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

@login_required
@csrf_exempt
def project_ajax_create(request):
    """AJAX create project"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['title', 'description', 'technologies', 'start_date', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Create project
            project = Project.objects.create(
                profile=profile,
                title=data['title'],
                description=data['description'],
                short_description=data.get('short_description', ''),
                technologies=data['technologies'],
                features=data.get('features', ''),
                challenges=data.get('challenges', ''),
                solutions=data.get('solutions', ''),
                github_url=data.get('github_url', ''),
                live_url=data.get('live_url', ''),
                video_url=data.get('video_url', ''),
                start_date=data['start_date'],
                end_date=data.get('end_date', None),
                status=data.get('status', 'completed'),
                is_featured=data.get('is_featured', False),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Project created successfully!',
                'project_id': str(project.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def project_ajax_update(request, project_id):
    """AJAX update project"""
    if request.method == 'POST':
        try:
            project = get_object_or_404(Project, id=project_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['title', 'description', 'technologies', 'start_date', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Update project
            project.profile = profile
            project.title = data['title']
            project.description = data['description']
            project.short_description = data.get('short_description', '')
            project.technologies = data['technologies']
            project.features = data.get('features', '')
            project.challenges = data.get('challenges', '')
            project.solutions = data.get('solutions', '')
            project.github_url = data.get('github_url', '')
            project.live_url = data.get('live_url', '')
            project.video_url = data.get('video_url', '')
            project.start_date = data['start_date']
            project.end_date = data.get('end_date', None)
            project.status = data.get('status', 'completed')
            project.is_featured = data.get('is_featured', False)
            project.is_active = data.get('is_active', True)
            project.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Project updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def project_ajax_delete(request, project_id):
    """AJAX delete project"""
    if request.method == 'POST':
        try:
            project = get_object_or_404(Project, id=project_id)
            
            # Delete associated files
            delete_file_if_exists(project.image)
            
            project.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Project deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def project_toggle_status(request, project_id):
    """Toggle project status"""
    try:
        project = get_object_or_404(Project, id=project_id)
        project.is_active = not project.is_active
        project.save()
        
        status = 'activated' if project.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Project {status} successfully!',
            'is_active': project.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def project_toggle_featured(request, project_id):
    """Toggle project featured status"""
    try:
        project = get_object_or_404(Project, id=project_id)
        project.is_featured = not project.is_featured
        project.save()
        
        status = 'featured' if project.is_featured else 'unfeatured'
        
        return JsonResponse({
            'success': True,
            'message': f'Project {status} successfully!',
            'is_featured': project.is_featured
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# EXPERIENCE VIEWS
# ============================================================================

@login_required
def experience_list(request):
    """List all experiences"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        
        experiences = Experience.objects.all().order_by('-start_date')
        
        if search_query:
            experiences = experiences.filter(
                Q(company__icontains=search_query) |
                Q(position__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(responsibilities__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                experiences = experiences.filter(is_active=True)
            elif status_filter == 'inactive':
                experiences = experiences.filter(is_active=False)
            elif status_filter == 'current':
                experiences = experiences.filter(is_current=True)
        
        if profile_filter:
            experiences = experiences.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(experiences, 10)  # Show 10 experiences per page
        page_number = request.GET.get('page')
        experiences_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'experiences_list': experiences_list,
            'profiles': profiles,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'page_title': 'Experience Management',
            'active_menu': 'experiences'
        }
        
        return render(request, 'custom_admin/experience/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading experiences: {str(e)}')
        return render(request, 'custom_admin/experience/list.html', {'error': str(e)})

@login_required
def experience_modal_create(request):
    """
    Render the create experience modal form fields
    """
    context = {
        'profiles': Profile.objects.filter(is_active=True),
    }
    return render(request, 'custom_admin/experience/modal_form_fields.html', context)

@login_required
def experience_modal_edit(request, pk):
    """
    Render the edit experience modal form fields
    """
    try:
        experience = Experience.objects.get(pk=pk)
        context = {
            'experience': experience,
            'profiles': Profile.objects.filter(is_active=True),
        }
        return render(request, 'custom_admin/experience/modal_form_fields.html', context)
    except Experience.DoesNotExist:
        return JsonResponse({'error': 'Experience not found'}, status=404)

@login_required
@csrf_exempt
def experience_ajax_create(request):
    """AJAX create experience"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['company', 'position', 'description', 'start_date', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Create experience
            experience = Experience.objects.create(
                profile=profile,
                company=data['company'],
                position=data['position'],
                description=data['description'],
                responsibilities=data.get('responsibilities', ''),
                achievements=data.get('achievements', ''),
                start_date=data['start_date'],
                end_date=data.get('end_date', None),
                is_current=data.get('is_current', False),
                company_url=data.get('company_url', ''),
                location=data.get('location', ''),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Experience created successfully!',
                'experience_id': str(experience.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def experience_ajax_update(request, experience_id):
    """AJAX update experience"""
    if request.method == 'POST':
        try:
            experience = get_object_or_404(Experience, id=experience_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['company', 'position', 'description', 'start_date', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Update experience
            experience.profile = profile
            experience.company = data['company']
            experience.position = data['position']
            experience.description = data['description']
            experience.responsibilities = data.get('responsibilities', '')
            experience.achievements = data.get('achievements', '')
            experience.start_date = data['start_date']
            experience.end_date = data.get('end_date', None)
            experience.is_current = data.get('is_current', False)
            experience.company_url = data.get('company_url', '')
            experience.location = data.get('location', '')
            experience.is_active = data.get('is_active', True)
            experience.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Experience updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def experience_ajax_delete(request, experience_id):
    """AJAX delete experience"""
    if request.method == 'POST':
        try:
            experience = get_object_or_404(Experience, id=experience_id)
            
            # Delete associated files
            delete_file_if_exists(experience.company_logo)
            
            experience.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Experience deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def experience_toggle_status(request, experience_id):
    """Toggle experience status"""
    try:
        experience = get_object_or_404(Experience, id=experience_id)
        experience.is_active = not experience.is_active
        experience.save()
        
        status = 'activated' if experience.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Experience {status} successfully!',
            'is_active': experience.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def experience_toggle_current(request, experience_id):
    """Toggle experience current status"""
    try:
        experience = get_object_or_404(Experience, id=experience_id)
        experience.is_current = not experience.is_current
        
        # If marked as current, remove end date
        if experience.is_current:
            experience.end_date = None
        
        experience.save()
        
        status = 'marked as current' if experience.is_current else 'unmarked as current'
        
        return JsonResponse({
            'success': True,
            'message': f'Experience {status} successfully!',
            'is_current': experience.is_current
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# CERTIFICATE VIEWS
# ============================================================================

@login_required
def certificate_list(request):
    """List all certificates"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        
        certificates = Certificate.objects.all().order_by('-issue_date')
        
        if search_query:
            certificates = certificates.filter(
                Q(name__icontains=search_query) |
                Q(issuing_organization__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(credential_id__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                certificates = certificates.filter(is_active=True)
            elif status_filter == 'inactive':
                certificates = certificates.filter(is_active=False)
        
        if profile_filter:
            certificates = certificates.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(certificates, 10)  # Show 10 certificates per page
        page_number = request.GET.get('page')
        certificates_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'certificates_list': certificates_list,
            'profiles': profiles,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'page_title': 'Certificate Management',
            'active_menu': 'certificates'
        }
        
        return render(request, 'custom_admin/certificates/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading certificates: {str(e)}')
        return render(request, 'custom_admin/certificates/list.html', {'error': str(e)})

@login_required
def certificate_detail(request, pk):
    """View certificate details"""
    try:
        certificate = get_object_or_404(Certificate, pk=pk)
        context = {
            'certificate': certificate,
            'page_title': f'Certificate: {certificate.name}',
            'active_menu': 'certificates'
        }
        return render(request, 'custom_admin/certificates/detail.html', context)
    except Exception as e:
        messages.error(request, f'Error loading certificate: {str(e)}')
        return redirect('certificate_list')

@login_required
def certificate_modal_create(request):
    """
    Render the create certificate modal form fields
    """
    context = {
        'profiles': Profile.objects.filter(is_active=True),
    }
    return render(request, 'custom_admin/certificates/modal_form_fields.html', context)

@login_required
def certificate_modal_edit(request, pk):
    """
    Render the edit certificate modal form fields
    """
    try:
        certificate = Certificate.objects.get(pk=pk)
        context = {
            'certificate': certificate,
            'profiles': Profile.objects.filter(is_active=True),
        }
        return render(request, 'custom_admin/certificates/modal_form_fields.html', context)
    except Certificate.DoesNotExist:
        return JsonResponse({'error': 'Certificate not found'}, status=404)

@login_required
@csrf_exempt
def certificate_ajax_create(request):
    """AJAX create certificate"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'issuing_organization', 'issue_date', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Create certificate
            certificate = Certificate.objects.create(
                profile=profile,
                name=data['name'],
                issuing_organization=data['issuing_organization'],
                description=data.get('description', ''),
                issue_date=data['issue_date'],
                expiration_date=data.get('expiration_date', None),
                credential_id=data.get('credential_id', ''),
                credential_url=data.get('credential_url', ''),
                skills=data.get('skills', ''),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Certificate created successfully!',
                'certificate_id': str(certificate.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def certificate_ajax_update(request, certificate_id):
    """AJAX update certificate"""
    if request.method == 'POST':
        try:
            certificate = get_object_or_404(Certificate, id=certificate_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'issuing_organization', 'issue_date', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Update certificate
            certificate.profile = profile
            certificate.name = data['name']
            certificate.issuing_organization = data['issuing_organization']
            certificate.description = data.get('description', '')
            certificate.issue_date = data['issue_date']
            certificate.expiration_date = data.get('expiration_date', None)
            certificate.credential_id = data.get('credential_id', '')
            certificate.credential_url = data.get('credential_url', '')
            certificate.skills = data.get('skills', '')
            certificate.is_active = data.get('is_active', True)
            certificate.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Certificate updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def certificate_ajax_delete(request, certificate_id):
    """AJAX delete certificate"""
    if request.method == 'POST':
        try:
            certificate = get_object_or_404(Certificate, id=certificate_id)
            
            # Delete associated files
            delete_file_if_exists(certificate.image)
            delete_file_if_exists(certificate.certificate_file)
            
            certificate.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Certificate deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def certificate_toggle_status(request, certificate_id):
    """Toggle certificate status"""
    try:
        certificate = get_object_or_404(Certificate, id=certificate_id)
        certificate.is_active = not certificate.is_active
        certificate.save()
        
        status = 'activated' if certificate.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Certificate {status} successfully!',
            'is_active': certificate.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# EDUCATION VIEWS
# ============================================================================

@login_required
def education_list(request):
    """List all education entries"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        
        educations = Education.objects.all().order_by('-end_date')
        
        if search_query:
            educations = educations.filter(
                Q(institution__icontains=search_query) |
                Q(degree__icontains=search_query) |
                Q(field_of_study__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                educations = educations.filter(is_active=True)
            elif status_filter == 'inactive':
                educations = educations.filter(is_active=False)
        
        if profile_filter:
            educations = educations.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(educations, 10)  # Show 10 education entries per page
        page_number = request.GET.get('page')
        educations_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'educations_list': educations_list,
            'profiles': profiles,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'page_title': 'Education Management',
            'active_menu': 'education'
        }
        
        return render(request, 'custom_admin/education/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading education entries: {str(e)}')
        return render(request, 'custom_admin/education/list.html', {'error': str(e)})

@login_required
def education_modal_create(request):
    """
    Render the create education modal form fields
    """
    context = {
        'profiles': Profile.objects.filter(is_active=True),
    }
    return render(request, 'custom_admin/education/modal_form_fields.html', context)

@login_required
def education_modal_edit(request, pk):
    """
    Render the edit education modal form fields
    """
    try:
        education = Education.objects.get(pk=pk)
        context = {
            'education': education,
            'profiles': Profile.objects.filter(is_active=True),
        }
        return render(request, 'custom_admin/education/modal_form_fields.html', context)
    except Education.DoesNotExist:
        return JsonResponse({'error': 'Education not found'}, status=404)

@login_required
@csrf_exempt
def education_ajax_create(request):
    """AJAX create education"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['institution', 'degree', 'field_of_study', 'start_date', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Create education
            education = Education.objects.create(
                profile=profile,
                institution=data['institution'],
                degree=data['degree'],
                field_of_study=data['field_of_study'],
                description=data.get('description', ''),
                start_date=data['start_date'],
                end_date=data.get('end_date', None),
                gpa=data.get('gpa', ''),
                achievements=data.get('achievements', ''),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Education created successfully!',
                'education_id': str(education.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def education_ajax_update(request, education_id):
    """AJAX update education"""
    if request.method == 'POST':
        try:
            education = get_object_or_404(Education, id=education_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['institution', 'degree', 'field_of_study', 'start_date', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Update education
            education.profile = profile
            education.institution = data['institution']
            education.degree = data['degree']
            education.field_of_study = data['field_of_study']
            education.description = data.get('description', '')
            education.start_date = data['start_date']
            education.end_date = data.get('end_date', None)
            education.gpa = data.get('gpa', '')
            education.achievements = data.get('achievements', '')
            education.is_active = data.get('is_active', True)
            education.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Education updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def education_ajax_delete(request, education_id):
    """AJAX delete education"""
    if request.method == 'POST':
        try:
            education = get_object_or_404(Education, id=education_id)
            
            # Delete associated files
            delete_file_if_exists(education.logo)
            delete_file_if_exists(education.certificate)
            
            education.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Education deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def education_toggle_status(request, education_id):
    """Toggle education status"""
    try:
        education = get_object_or_404(Education, id=education_id)
        education.is_active = not education.is_active
        education.save()
        
        status = 'activated' if education.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Education {status} successfully!',
            'is_active': education.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# AWARD VIEWS
# ============================================================================

@login_required
def award_list(request):
    """List all awards"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        
        awards = Award.objects.all().order_by('-date_received')
        
        if search_query:
            awards = awards.filter(
                Q(title__icontains=search_query) |
                Q(issuer__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                awards = awards.filter(is_active=True)
            elif status_filter == 'inactive':
                awards = awards.filter(is_active=False)
            elif status_filter == 'featured':
                awards = awards.filter(is_featured=True)
        
        if profile_filter:
            awards = awards.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(awards, 10)  # Show 10 awards per page
        page_number = request.GET.get('page')
        awards_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'awards_list': awards_list,
            'profiles': profiles,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'page_title': 'Award Management',
            'active_menu': 'awards'
        }
        
        return render(request, 'custom_admin/awards/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading awards: {str(e)}')
        return render(request, 'custom_admin/awards/list.html', {'error': str(e)})

@login_required
def award_modal_create(request):
    """
    Render the create award modal form fields
    """
    context = {
        'profiles': Profile.objects.filter(is_active=True),
    }
    return render(request, 'custom_admin/awards/modal_form_fields.html', context)

@login_required
def award_modal_edit(request, pk):
    """
    Render the edit award modal form fields
    """
    try:
        award = Award.objects.get(pk=pk)
        context = {
            'award': award,
            'profiles': Profile.objects.filter(is_active=True),
        }
        return render(request, 'custom_admin/awards/modal_form_fields.html', context)
    except Award.DoesNotExist:
        return JsonResponse({'error': 'Award not found'}, status=404)

@login_required
@csrf_exempt
def award_ajax_create(request):
    """AJAX create award"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['title', 'issuer', 'date_received', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Create award
            award = Award.objects.create(
                profile=profile,
                title=data['title'],
                issuer=data['issuer'],
                description=data.get('description', ''),
                date_received=data['date_received'],
                url=data.get('url', ''),
                is_featured=data.get('is_featured', False),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Award created successfully!',
                'award_id': str(award.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def award_ajax_update(request, award_id):
    """AJAX update award"""
    if request.method == 'POST':
        try:
            award = get_object_or_404(Award, id=award_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['title', 'issuer', 'date_received', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Update award
            award.profile = profile
            award.title = data['title']
            award.issuer = data['issuer']
            award.description = data.get('description', '')
            award.date_received = data['date_received']
            award.url = data.get('url', '')
            award.is_featured = data.get('is_featured', False)
            award.is_active = data.get('is_active', True)
            award.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Award updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def award_ajax_delete(request, award_id):
    """AJAX delete award"""
    if request.method == 'POST':
        try:
            award = get_object_or_404(Award, id=award_id)
            
            # Delete associated files
            delete_file_if_exists(award.image)
            delete_file_if_exists(award.certificate)
            
            award.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Award deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def award_toggle_status(request, award_id):
    """Toggle award status"""
    try:
        award = get_object_or_404(Award, id=award_id)
        award.is_active = not award.is_active
        award.save()
        
        status = 'activated' if award.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Award {status} successfully!',
            'is_active': award.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def award_toggle_featured(request, award_id):
    """Toggle award featured status"""
    try:
        award = get_object_or_404(Award, id=award_id)
        award.is_featured = not award.is_featured
        award.save()
        
        status = 'featured' if award.is_featured else 'unfeatured'
        
        return JsonResponse({
            'success': True,
            'message': f'Award {status} successfully!',
            'is_featured': award.is_featured
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# SERVICE VIEWS
# ============================================================================

@login_required
def service_list(request):
    """List all services"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        
        services = Service.objects.all().order_by('-created_at')
        
        if search_query:
            services = services.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                services = services.filter(is_active=True)
            elif status_filter == 'inactive':
                services = services.filter(is_active=False)
            elif status_filter == 'featured':
                services = services.filter(is_featured=True)
        
        if profile_filter:
            services = services.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(services, 10)  # Show 10 services per page
        page_number = request.GET.get('page')
        services_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'services_list': services_list,
            'profiles': profiles,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'page_title': 'Service Management',
            'active_menu': 'services'
        }
        
        return render(request, 'custom_admin/services/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading services: {str(e)}')
        return render(request, 'custom_admin/services/list.html', {'error': str(e)})

@login_required
def service_modal_create(request):
    """
    Render the create service modal form fields
    """
    context = {
        'profiles': Profile.objects.filter(is_active=True),
    }
    return render(request, 'custom_admin/services/modal_form_fields.html', context)

@login_required
def service_modal_edit(request, pk):
    """
    Render the edit service modal form fields
    """
    try:
        service = Service.objects.get(pk=pk)
        context = {
            'service': service,
            'profiles': Profile.objects.filter(is_active=True),
        }
        return render(request, 'custom_admin/services/modal_form_fields.html', context)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)

@login_required
@csrf_exempt
def service_ajax_create(request):
    """AJAX create service"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['title', 'description', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Create service
            service = Service.objects.create(
                profile=profile,
                title=data['title'],
                description=data['description'],
                icon=data.get('icon', ''),
                is_featured=data.get('is_featured', False),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Service created successfully!',
                'service_id': str(service.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def service_ajax_update(request, service_id):
    """AJAX update service"""
    if request.method == 'POST':
        try:
            service = get_object_or_404(Service, id=service_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['title', 'description', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Update service
            service.profile = profile
            service.title = data['title']
            service.description = data['description']
            service.icon = data.get('icon', '')
            service.is_featured = data.get('is_featured', False)
            service.is_active = data.get('is_active', True)
            service.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Service updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def service_ajax_delete(request, service_id):
    """AJAX delete service"""
    if request.method == 'POST':
        try:
            service = get_object_or_404(Service, id=service_id)
            service.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Service deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def service_toggle_status(request, service_id):
    """Toggle service status"""
    try:
        service = get_object_or_404(Service, id=service_id)
        service.is_active = not service.is_active
        service.save()
        
        status = 'activated' if service.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Service {status} successfully!',
            'is_active': service.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def service_toggle_featured(request, service_id):
    """Toggle service featured status"""
    try:
        service = get_object_or_404(Service, id=service_id)
        service.is_featured = not service.is_featured
        service.save()
        
        status = 'featured' if service.is_featured else 'unfeatured'
        
        return JsonResponse({
            'success': True,
            'message': f'Service {status} successfully!',
            'is_featured': service.is_featured
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# TESTIMONIAL VIEWS
# ============================================================================

@login_required
def testimonial_list(request):
    """List all testimonials"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        
        testimonials = Testimonial.objects.all().order_by('-created_at')
        
        if search_query:
            testimonials = testimonials.filter(
                Q(name__icontains=search_query) |
                Q(position__icontains=search_query) |
                Q(company__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'active':
                testimonials = testimonials.filter(is_active=True)
            elif status_filter == 'inactive':
                testimonials = testimonials.filter(is_active=False)
            elif status_filter == 'featured':
                testimonials = testimonials.filter(is_featured=True)
        
        if profile_filter:
            testimonials = testimonials.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(testimonials, 10)  # Show 10 testimonials per page
        page_number = request.GET.get('page')
        testimonials_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'testimonials_list': testimonials_list,
            'profiles': profiles,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'page_title': 'Testimonial Management',
            'active_menu': 'testimonials'
        }
        
        return render(request, 'custom_admin/testimonials/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading testimonials: {str(e)}')
        return render(request, 'custom_admin/testimonials/list.html', {'error': str(e)})

@login_required
def testimonial_modal_create(request):
    """
    Render the create testimonial modal form fields
    """
    context = {
        'profiles': Profile.objects.filter(is_active=True),
    }
    return render(request, 'custom_admin/testimonials/modal_form_fields.html', context)

@login_required
def testimonial_modal_edit(request, pk):
    """
    Render the edit testimonial modal form fields
    """
    try:
        testimonial = Testimonial.objects.get(pk=pk)
        context = {
            'testimonial': testimonial,
            'profiles': Profile.objects.filter(is_active=True),
        }
        return render(request, 'custom_admin/testimonials/modal_form_fields.html', context)
    except Testimonial.DoesNotExist:
        return JsonResponse({'error': 'Testimonial not found'}, status=404)

@login_required
@csrf_exempt
def testimonial_ajax_create(request):
    """AJAX create testimonial"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'content', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Create testimonial
            testimonial = Testimonial.objects.create(
                profile=profile,
                name=data['name'],
                position=data.get('position', ''),
                company=data.get('company', ''),
                content=data['content'],
                rating=data.get('rating', 5),
                is_featured=data.get('is_featured', False),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Testimonial created successfully!',
                'testimonial_id': str(testimonial.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def testimonial_ajax_update(request, testimonial_id):
    """AJAX update testimonial"""
    if request.method == 'POST':
        try:
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'content', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Update testimonial
            testimonial.profile = profile
            testimonial.name = data['name']
            testimonial.position = data.get('position', '')
            testimonial.company = data.get('company', '')
            testimonial.content = data['content']
            testimonial.rating = data.get('rating', 5)
            testimonial.is_featured = data.get('is_featured', False)
            testimonial.is_active = data.get('is_active', True)
            testimonial.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Testimonial updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def testimonial_ajax_delete(request, testimonial_id):
    """AJAX delete testimonial"""
    if request.method == 'POST':
        try:
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            
            # Delete associated files
            delete_file_if_exists(testimonial.avatar)
            
            testimonial.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Testimonial deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def testimonial_toggle_status(request, testimonial_id):
    """Toggle testimonial status"""
    try:
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
        testimonial.is_active = not testimonial.is_active
        testimonial.save()
        
        status = 'activated' if testimonial.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Testimonial {status} successfully!',
            'is_active': testimonial.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def testimonial_toggle_featured(request, testimonial_id):
    """Toggle testimonial featured status"""
    try:
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
        testimonial.is_featured = not testimonial.is_featured
        testimonial.save()
        
        status = 'featured' if testimonial.is_featured else 'unfeatured'
        
        return JsonResponse({
            'success': True,
            'message': f'Testimonial {status} successfully!',
            'is_featured': testimonial.is_featured
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# CONTACT VIEWS
# ============================================================================

@login_required
def contact_list(request):
    """List all contacts"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        profile_filter = request.GET.get('profile', '')
        
        contacts = Contact.objects.all().order_by('-created_at')
        
        if search_query:
            contacts = contacts.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(subject__icontains=search_query) |
                Q(message__icontains=search_query)
            )
        
        if status_filter:
            if status_filter == 'read':
                contacts = contacts.filter(status='read')
            elif status_filter == 'unread':
                contacts = contacts.filter(status='new')
        
        if profile_filter:
            contacts = contacts.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(contacts, 10)  # Show 10 contacts per page
        page_number = request.GET.get('page')
        contacts_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'contacts_list': contacts_list,
            'profiles': profiles,
            'search_query': search_query,
            'status_filter': status_filter,
            'profile_filter': profile_filter,
            'page_title': 'Contact Management',
            'active_menu': 'contacts'
        }
        
        return render(request, 'custom_admin/contacts/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading contacts: {str(e)}')
        return render(request, 'custom_admin/contacts/list.html', {'error': str(e)})

@login_required
def contact_detail(request, pk):
    """View contact details"""
    try:
        contact = get_object_or_404(Contact, pk=pk)
        
        # Mark as read if not already read
        if contact.status == 'new':
            contact.status = 'read'
            contact.save()
        
        context = {
            'contact': contact,
            'page_title': 'Contact Details',
            'active_menu': 'contacts'
        }
        
        return render(request, 'custom_admin/contacts/detail.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading contact details: {str(e)}')
        return redirect('contact_list')

@login_required
@csrf_exempt
def contact_ajax_delete(request, contact_id):
    """AJAX delete contact"""
    if request.method == 'POST':
        try:
            contact = get_object_or_404(Contact, id=contact_id)
            contact.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Contact deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def contact_mark_as_read(request, contact_id):
    """Mark contact as read"""
    try:
        contact = get_object_or_404(Contact, id=contact_id)
        contact.status = 'read'
        contact.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Contact marked as read successfully!',
            'is_read': contact.status == 'read'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def contact_mark_as_unread(request, contact_id):
    """Mark contact as unread"""
    try:
        contact = get_object_or_404(Contact, id=contact_id)
        contact.status = 'new'
        contact.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Contact marked as unread successfully!',
            'is_read': contact.status == 'read'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# ABOUT VIEWS
# ============================================================================

@login_required
def about_list(request):
    """List all about entries"""
    try:
        profile_filter = request.GET.get('profile', '')
        
        abouts = About.objects.all().order_by('-updated_at')
        
        if profile_filter:
            abouts = abouts.filter(profile_id=profile_filter)
        
        # Pagination
        paginator = Paginator(abouts, 10)  # Show 10 about entries per page
        page_number = request.GET.get('page')
        abouts_list = paginator.get_page(page_number)
        
        # Get available profiles
        profiles = Profile.objects.filter(is_active=True)
        
        context = {
            'abouts_list': abouts_list,
            'profiles': profiles,
            'profile_filter': profile_filter,
            'page_title': 'About Management',
            'active_menu': 'about'
        }
        
        return render(request, 'custom_admin/about/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading about entries: {str(e)}')
        return render(request, 'custom_admin/about/list.html', {'error': str(e)})

@login_required
def about_detail(request, pk):
    """View about details"""
    try:
        about = get_object_or_404(About, pk=pk)
        
        context = {
            'about': about,
            'page_title': 'About Details',
            'active_menu': 'about'
        }
        
        return render(request, 'custom_admin/about/detail.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading about details: {str(e)}')
        return redirect('about_list')

@login_required
def about_modal_create(request):
    """
    Render the create about modal form fields
    """
    context = {
        'profiles': Profile.objects.filter(is_active=True),
    }
    return render(request, 'custom_admin/about/modal_form_fields.html', context)

@login_required
def about_modal_edit(request, pk):
    """
    Render the edit about modal form fields
    """
    try:
        about = About.objects.get(pk=pk)
        context = {
            'about': about,
            'profiles': Profile.objects.filter(is_active=True),
        }
        return render(request, 'custom_admin/about/modal_form_fields.html', context)
    except About.DoesNotExist:
        return JsonResponse({'error': 'About not found'}, status=404)

@login_required
@csrf_exempt
def about_ajax_create(request):
    """AJAX create about"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['story_title', 'story_content', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Check if about already exists for this profile
            if About.objects.filter(profile=profile).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'About entry already exists for this profile'
                })
            
            # Create about
            about = About.objects.create(
                profile=profile,
                story_title=data['story_title'],
                story_content=data['story_content'],
                mission=data.get('mission', ''),
                vision=data.get('vision', ''),
                values=data.get('values', ''),
                hobbies=data.get('hobbies', ''),
                languages=data.get('languages', ''),
                is_active=data.get('is_active', True)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'About created successfully!',
                'about_id': str(about.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def about_ajax_update(request, about_id):
    """AJAX update about"""
    if request.method == 'POST':
        try:
            about = get_object_or_404(About, id=about_id)
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['story_title', 'story_content', 'profile']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({
                        'success': False,
                        'error': f'Field {field} is required'
                    })
            
            # Get profile
            profile = get_object_or_404(Profile, id=data['profile'])
            
            # Check if about already exists for this profile (if changing profile)
            if about.profile != profile and About.objects.filter(profile=profile).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'About entry already exists for this profile'
                })
            
            # Update about
            about.profile = profile
            about.story_title = data['story_title']
            about.story_content = data['story_content']
            about.mission = data.get('mission', '')
            about.vision = data.get('vision', '')
            about.values = data.get('values', '')
            about.hobbies = data.get('hobbies', '')
            about.languages = data.get('languages', '')
            about.is_active = data.get('is_active', True)
            about.save()
            
            return JsonResponse({
                'success': True,
                'message': 'About updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def about_ajax_delete(request, about_id):
    """AJAX delete about"""
    if request.method == 'POST':
        try:
            about = get_object_or_404(About, id=about_id)
            about.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'About deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def about_toggle_status(request, about_id):
    """Toggle about status"""
    try:
        about = get_object_or_404(About, id=about_id)
        about.is_active = not about.is_active
        about.save()
        
        status = 'activated' if about.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'About {status} successfully!',
            'is_active': about.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

# ============================================================================
# PROFILE VIEWS
# ============================================================================

@login_required
def profile_list(request):
    """List all profiles"""
    try:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        
        profiles = Profile.objects.all().order_by('-updated_at')
        
        # Apply search filter
        if search_query:
            profiles = profiles.filter(
                Q(name__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        
        # Apply status filter
        if status_filter:
            is_active = status_filter == 'active'
            profiles = profiles.filter(is_active=is_active)
        
        # Pagination
        paginator = Paginator(profiles, 10)  # Show 10 profiles per page
        page_number = request.GET.get('page')
        profiles_list = paginator.get_page(page_number)
        
        context = {
            'profiles_list': profiles_list,
            'search_query': search_query,
            'status_filter': status_filter,
            'page_title': 'Profile Management',
            'active_menu': 'profile'
        }
        
        return render(request, 'custom_admin/profile/list.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading profiles: {str(e)}')
        return render(request, 'custom_admin/profile/list.html', {'error': str(e)})

@login_required
def profile_detail(request, pk):
    """View profile details"""
    try:
        profile = get_object_or_404(Profile, pk=pk)
        
        context = {
            'profile': profile,
            'page_title': 'Profile Details',
            'active_menu': 'profile'
        }
        
        return render(request, 'custom_admin/profile/detail.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading profile details: {str(e)}')
        return redirect('profile_list')

@login_required
def profile_modal_create(request):
    """
    Render the create profile modal form fields
    """
    return render(request, 'custom_admin/profile/modal_form_fields.html')

@login_required
def profile_modal_edit(request, pk):
    """
    Render the edit profile modal form fields
    """
    try:
        profile = Profile.objects.get(pk=pk)
        context = {
            'profile': profile
        }
        return render(request, 'custom_admin/profile/modal_form_fields.html', context)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

@login_required
@csrf_exempt
def profile_ajax_create(request):
    """AJAX create profile"""
    if request.method == 'POST':
        try:
            # Handle file uploads
            profile_image = request.FILES.get('profile_image')
            resume_file = request.FILES.get('resume')
            
            # Get form data
            name = request.POST.get('name')
            title = request.POST.get('title')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            bio = request.POST.get('bio')
            facebook = request.POST.get('facebook', '')
            twitter = request.POST.get('twitter', '')
            linkedin = request.POST.get('linkedin', '')
            github = request.POST.get('github', '')
            instagram = request.POST.get('instagram', '')
            youtube = request.POST.get('youtube', '')
            is_active = request.POST.get('is_active') == 'on'
            
            # Validate required fields
            if not name or not title or not email:
                return JsonResponse({
                    'success': False,
                    'error': 'Name, title, and email are required fields'
                })
            
            # Create profile
            profile = Profile.objects.create(
                name=name,
                title=title,
                email=email,
                phone=phone,
                address=address,
                bio=bio,
                facebook=facebook,
                twitter=twitter,
                linkedin=linkedin,
                github=github,
                instagram=instagram,
                youtube=youtube,
                is_active=is_active
            )
            
            # Handle file uploads
            if profile_image:
                profile.profile_image = profile_image
            
            if resume_file:
                profile.resume = resume_file
            
            profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Profile created successfully!',
                'profile_id': str(profile.id)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def profile_ajax_update(request, profile_id):
    """AJAX update profile"""
    if request.method == 'POST':
        try:
            profile = get_object_or_404(Profile, id=profile_id)
            
            # Get form data
            profile.name = request.POST.get('name')
            profile.title = request.POST.get('title')
            profile.email = request.POST.get('email')
            profile.phone = request.POST.get('phone')
            profile.address = request.POST.get('address')
            profile.bio = request.POST.get('bio')
            profile.facebook = request.POST.get('facebook', '')
            profile.twitter = request.POST.get('twitter', '')
            profile.linkedin = request.POST.get('linkedin', '')
            profile.github = request.POST.get('github', '')
            profile.instagram = request.POST.get('instagram', '')
            profile.youtube = request.POST.get('youtube', '')
            profile.is_active = request.POST.get('is_active') == 'on'
            
            # Handle file uploads
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                # Delete old image if exists
                if profile.profile_image:
                    try:
                        profile.profile_image.delete()
                    except Exception:
                        pass
                profile.profile_image = profile_image
            
            resume_file = request.FILES.get('resume')
            if resume_file:
                # Delete old resume if exists
                if profile.resume:
                    try:
                        profile.resume.delete()
                    except Exception:
                        pass
                profile.resume = resume_file
            
            # Validate required fields
            if not profile.name or not profile.title or not profile.email:
                return JsonResponse({
                    'success': False,
                    'error': 'Name, title, and email are required fields'
                })
            
            profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def profile_ajax_delete(request, profile_id):
    """AJAX delete profile"""
    if request.method == 'POST':
        try:
            profile = get_object_or_404(Profile, id=profile_id)
            
            # Delete associated files
            if profile.profile_image:
                try:
                    profile.profile_image.delete()
                except Exception:
                    pass
            
            if profile.resume:
                try:
                    profile.resume.delete()
                except Exception:
                    pass
            
            profile.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Profile deleted successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def profile_toggle_status(request, profile_id):
    """Toggle profile status"""
    try:
        profile = get_object_or_404(Profile, id=profile_id)
        profile.is_active = not profile.is_active
        profile.save()
        
        status = 'activated' if profile.is_active else 'deactivated'
        
        return JsonResponse({
            'success': True,
            'message': f'Profile {status} successfully!',
            'is_active': profile.is_active
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
@csrf_exempt
def skill_toggle_featured(request, skill_id):
    """Toggle skill featured status"""
    try:
        skill = get_object_or_404(Skill, id=skill_id)
        skill.is_featured = not skill.is_featured
        skill.save()
        
        status = 'featured' if skill.is_featured else 'unfeatured'
        
        return JsonResponse({
            'success': True,
            'message': f'Skill {status} successfully!',
            'is_featured': skill.is_featured
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })