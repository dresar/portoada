from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db.models import Q, Count
import json

from .models import (
    Profile, About, Education, Skill, Project, Experience,
    Certificate, Contact, Service, Testimonial, Blog, Award,
    BlogCategory, BlogTag, BlogComment, SocialMedia, PortfolioSettings
)
from .forms import (
    ProfileForm, AboutForm, EducationForm, SkillForm, ProjectForm, ExperienceForm,
    CertificateForm, ContactForm, ServiceForm, TestimonialForm, BlogForm, AwardForm,
    BlogCategoryForm, BlogTagForm, BlogCommentForm, SocialMediaForm, PortfolioSettingsForm
)
from .utils import render_form_to_json_response, prepare_list_view_context, prepare_detail_view_context
from .auth import admin_required
import os
from django.views.decorators.csrf import csrf_exempt

# Dashboard view
@admin_required
def dashboard(request):
    profile_count = Profile.objects.count()
    project_count = Project.objects.count()
    blog_count = Blog.objects.count()
    contact_count = Contact.objects.count()
    unread_messages = Contact.objects.filter(is_read=False).count()
    skill_count = Skill.objects.count()
    experience_count = Experience.objects.count()
    
    recent_projects = Project.objects.order_by('-created_at')[:5]
    recent_blogs = Blog.objects.order_by('-created_at')[:5]
    recent_messages = Contact.objects.order_by('-created_at')[:5]
    
    context = {
        'profile_count': profile_count,
        'project_count': project_count,
        'blog_count': blog_count,
        'contact_count': contact_count,
        'unread_messages': unread_messages,
        'skill_count': skill_count,
        'experience_count': experience_count,
        'recent_projects': recent_projects,
        'recent_blogs': recent_blogs,
        'recent_messages': recent_messages,
    }
    return render(request, 'portfolio_admin/dashboard.html', context)

# Preview views
@admin_required
def profile_preview(request):
    profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'profile_preview.html', {'profile': profile})

@admin_required
def about_preview(request):
    about = About.objects.filter(is_active=True).first()
    return render(request, 'about_preview.html', {'about': about})

@admin_required
def education_preview(request):
    educations = Education.objects.all().order_by('-start_date')
    return render(request, 'education_preview.html', {'educations': educations})

@admin_required
def skill_preview(request):
    skills = Skill.objects.all().order_by('category', '-proficiency')
    return render(request, 'skill_preview.html', {'skills': skills})

@admin_required
def project_preview(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'project_preview.html', {'projects': projects})

@admin_required
def experience_preview(request):
    experiences = Experience.objects.all().order_by('-start_date')
    return render(request, 'experience_preview.html', {'experiences': experiences})

@admin_required
def certificate_preview(request):
    certificates = Certificate.objects.all().order_by('-issue_date')
    return render(request, 'certificate_preview.html', {'certificates': certificates})

@admin_required
def service_preview(request):
    services = Service.objects.all()
    return render(request, 'service_preview.html', {'services': services})

@admin_required
def testimonial_preview(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'testimonial_preview.html', {'testimonials': testimonials})

@admin_required
def blog_preview(request):
    posts = Blog.objects.all().order_by('-created_at')
    categories = BlogCategory.objects.all()
    return render(request, 'blog_preview.html', {'posts': posts, 'categories': categories})

@admin_required
def award_preview(request):
    awards = Award.objects.all().order_by('-date_received')
    return render(request, 'award_preview.html', {'awards': awards})

@admin_required
def contact_preview(request):
    messages_list = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact_preview.html', {'messages': messages_list})

# Generic CRUD functions
def save_form(request, form, template_name, redirect_url=None):
    data = {}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            if redirect_url:
                data['redirect_url'] = redirect_url
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'form_url': request.path, 'form_title': 'Edit' if hasattr(form, 'instance') and form.instance.pk else 'Add'}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

# Profile Views
@admin_required
def profile_list(request):
    # Hanya tampilkan profil untuk user yang sedang login atau semua profil jika admin
    if request.user.is_superuser:
        profiles = Profile.objects.all()
    else:
        profiles = Profile.objects.filter(user=request.user)
    return render(request, 'portfolio_admin/profile/list.html', {'profiles': profiles})

@admin_required
def profile_create(request):
    # Cek apakah user sudah memiliki profil
    if Profile.objects.filter(user=request.user).exists():
        return JsonResponse({'status': 'error', 'message': 'You already have a profile'}, status=400)
        
    if request.method == 'POST':
        try:
            # Buat profil baru dengan user yang sedang login
            profile = Profile(
                user=request.user,
                title=request.POST.get('title'),
                bio=request.POST.get('bio'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                location=request.POST.get('location'),
                birth_date=request.POST.get('birth_date') or None
            )
            
            # Handle avatar upload
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
                
            profile.save()
            response_data = {'status': 'success', 'message': 'Profile created successfully'}
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return render(request, 'portfolio_admin/profile/create.html')

@admin_required
def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    
    # Pastikan user hanya dapat mengedit profil mereka sendiri kecuali superuser
    if not request.user.is_superuser and profile.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'You can only edit your own profile'}, status=403)
    
    if request.method == 'POST':
        try:
            # Update profil
            profile.title = request.POST.get('title')
            profile.bio = request.POST.get('bio')
            profile.email = request.POST.get('email')
            profile.phone = request.POST.get('phone')
            profile.location = request.POST.get('location')
            
            if request.POST.get('birth_date'):
                profile.birth_date = request.POST.get('birth_date')
            
            # Handle avatar upload
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
                
            profile.save()
            response_data = {'status': 'success', 'message': 'Profile updated successfully'}
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return render(request, 'portfolio_admin/profile/update.html', {'object': profile})

@admin_required
@require_POST
def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    
    # Pastikan user hanya dapat menghapus profil mereka sendiri kecuali superuser
    if not request.user.is_superuser and profile.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'You can only delete your own profile'}, status=403)
    
    try:
        profile.delete()
        return JsonResponse({'status': 'success', 'message': 'Profile deleted successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# About Views
@admin_required
def about_list(request):
    abouts = About.objects.all()
    return render(request, 'portfolio_admin/about/list.html', {'abouts': abouts})

@admin_required
def about_create(request):
    if request.method == 'POST':
        try:
            # Proses data form
            about = About(
                title=request.POST.get('title'),
                subtitle=request.POST.get('subtitle'),
                description=request.POST.get('description'),
                is_active=request.POST.get('is_active') == 'on'
            )
            
            # Handle image upload
            if 'image' in request.FILES:
                about.image = request.FILES['image']
                
            # Handle resume upload
            if 'resume' in request.FILES:
                about.resume = request.FILES['resume']
                
            # Jika is_active dicentang, nonaktifkan about lain
            if about.is_active:
                About.objects.filter(is_active=True).update(is_active=False)
                
            about.save()
            response_data = {'status': 'success', 'message': 'About created successfully'}
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return render(request, 'portfolio_admin/about/create.html')

@admin_required
def about_update(request, pk):
    about = get_object_or_404(About, pk=pk)
    if request.method == 'POST':
        try:
            # Update data
            about.title = request.POST.get('title')
            about.subtitle = request.POST.get('subtitle')
            about.description = request.POST.get('description')
            about.is_active = request.POST.get('is_active') == 'on'
            
            # Handle image upload
            if 'image' in request.FILES:
                about.image = request.FILES['image']
                
            # Handle resume upload
            if 'resume' in request.FILES:
                about.resume = request.FILES['resume']
                
            # Jika is_active dicentang, nonaktifkan about lain
            if about.is_active:
                About.objects.exclude(pk=about.pk).filter(is_active=True).update(is_active=False)
                
            about.save()
            response_data = {'status': 'success', 'message': 'About updated successfully'}
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return render(request, 'portfolio_admin/about/update.html', {'about': about})

@admin_required
@require_POST
def about_delete(request, pk):
    about = get_object_or_404(About, pk=pk)
    about.delete()
    return JsonResponse({'status': 'success', 'message': 'About deleted successfully'})

# Education Views
@admin_required
def education_list(request):
    educations = Education.objects.all().order_by('-start_date')
    return render(request, 'portfolio_admin/education/list.html', {'educations': educations})

@admin_required
def education_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Education created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/education/create.html')

@admin_required
def education_update(request, pk):
    education = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Education updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/education/update.html', {'education': education})

@admin_required
@require_POST
def education_delete(request, pk):
    education = get_object_or_404(Education, pk=pk)
    education.delete()
    return JsonResponse({'status': 'success', 'message': 'Education deleted successfully'})

# Skill Views
@admin_required
def skill_list(request):
    skills = Skill.objects.all().order_by('category', '-proficiency')
    return render(request, 'portfolio_admin/skill/list.html', {'skills': skills})

@admin_required
def skill_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Skill created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/skill/create.html')

@admin_required
def skill_update(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Skill updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/skill/update.html', {'skill': skill})

@admin_required
@require_POST
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    skill.delete()
    return JsonResponse({'status': 'success', 'message': 'Skill deleted successfully'})

# Project Views
@admin_required
def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'portfolio_admin/project/list.html', {'projects': projects})

@admin_required
def project_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Project created successfully'}
        return JsonResponse(response_data)
    skills = Skill.objects.all()
    return render(request, 'portfolio_admin/project/create.html', {'skills': skills})

@admin_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Project updated successfully'}
        return JsonResponse(response_data)
    skills = Skill.objects.all()
    return render(request, 'portfolio_admin/project/update.html', {'project': project, 'skills': skills})

@admin_required
@require_POST
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return JsonResponse({'status': 'success', 'message': 'Project deleted successfully'})

# Experience Views
@admin_required
def experience_list(request):
    experiences = Experience.objects.all().order_by('-start_date')
    return render(request, 'portfolio_admin/experience/list.html', {'experiences': experiences})

@admin_required
def experience_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Experience created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/experience/create.html')

@admin_required
def experience_update(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Experience updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/experience/update.html', {'experience': experience})

@admin_required
@require_POST
def experience_delete(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    experience.delete()
    return JsonResponse({'status': 'success', 'message': 'Experience deleted successfully'})

# Certificate Views
@admin_required
def certificate_list(request):
    certificates = Certificate.objects.all().order_by('-issue_date')
    return render(request, 'portfolio_admin/certificate/list.html', {'certificates': certificates})

@admin_required
def certificate_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Certificate created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/certificate/create.html')

@admin_required
def certificate_update(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Certificate updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/certificate/update.html', {'certificate': certificate})

@admin_required
@require_POST
def certificate_delete(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    certificate.delete()
    return JsonResponse({'status': 'success', 'message': 'Certificate deleted successfully'})

# Contact Views
@admin_required
def contact_list(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'portfolio_admin/contact/list.html', {'contacts': contacts})

@admin_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if not contact.is_read:
        contact.is_read = True
        contact.save()
    return render(request, 'portfolio_admin/contact/detail.html', {'contact': contact})

@admin_required
@require_POST
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return JsonResponse({'status': 'success', 'message': 'Contact deleted successfully'})

# Service Views
@admin_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'portfolio_admin/service/list.html', {'services': services})

@admin_required
def service_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Service created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/service/create.html')

@admin_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Service updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/service/update.html', {'service': service})

@admin_required
@require_POST
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return JsonResponse({'status': 'success', 'message': 'Service deleted successfully'})

# Testimonial Views
@admin_required
def testimonial_list(request):
    testimonials = Testimonial.objects.all().order_by('-created_at')
    return render(request, 'portfolio_admin/testimonial/list.html', {'testimonials': testimonials})

@admin_required
def testimonial_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Testimonial created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/testimonial/create.html')

@admin_required
def testimonial_update(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Testimonial updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/testimonial/update.html', {'testimonial': testimonial})

@admin_required
@require_POST
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    return JsonResponse({'status': 'success', 'message': 'Testimonial deleted successfully'})

# Blog Category Views
@admin_required
def blog_category_list(request):
    categories = BlogCategory.objects.all()
    return render(request, 'portfolio_admin/blog_category/list.html', {'categories': categories})

@admin_required
def blog_category_create(request):
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        slug = slugify(name)
        description = request.POST.get('description', '')
        
        category = BlogCategory.objects.create(
            name=name,
            slug=slug,
            description=description
        )
        
        response_data = {'status': 'success', 'message': 'Category created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/blog_category/create.html')

@admin_required
def blog_category_update(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        slug = slugify(name)
        description = request.POST.get('description', '')
        
        category.name = name
        category.slug = slug
        category.description = description
        category.save()
        
        response_data = {'status': 'success', 'message': 'Category updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/blog_category/update.html', {'category': category})

@admin_required
@require_POST
def blog_category_delete(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    category.delete()
    return JsonResponse({'status': 'success', 'message': 'Category deleted successfully'})

# Blog Tag Views
@admin_required
def blog_tag_list(request):
    tags = BlogTag.objects.all()
    return render(request, 'portfolio_admin/blog_tag/list.html', {'tags': tags})

@admin_required
def blog_tag_create(request):
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        slug = slugify(name)
        
        tag = BlogTag.objects.create(
            name=name,
            slug=slug
        )
        
        response_data = {'status': 'success', 'message': 'Tag created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/blog_tag/create.html')

@admin_required
def blog_tag_update(request, pk):
    tag = get_object_or_404(BlogTag, pk=pk)
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        slug = slugify(name)
        
        tag.name = name
        tag.slug = slug
        tag.save()
        
        response_data = {'status': 'success', 'message': 'Tag updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/blog_tag/update.html', {'tag': tag})

@admin_required
@require_POST
def blog_tag_delete(request, pk):
    tag = get_object_or_404(BlogTag, pk=pk)
    tag.delete()
    return JsonResponse({'status': 'success', 'message': 'Tag deleted successfully'})

# Blog Views
@admin_required
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'portfolio_admin/blog/list.html', {'blogs': blogs})

@admin_required
def blog_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Blog created successfully'}
        return JsonResponse(response_data)
    categories = BlogCategory.objects.all()
    tags = BlogTag.objects.all()
    return render(request, 'portfolio_admin/blog/create.html', {'categories': categories, 'tags': tags})

@admin_required
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Blog updated successfully'}
        return JsonResponse(response_data)
    categories = BlogCategory.objects.all()
    tags = BlogTag.objects.all()
    return render(request, 'portfolio_admin/blog/update.html', {'blog': blog, 'categories': categories, 'tags': tags})

@admin_required
@require_POST
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return JsonResponse({'status': 'success', 'message': 'Blog deleted successfully'})

# Blog Comment Views
@admin_required
def blog_comment_list(request):
    comments = BlogComment.objects.all().order_by('-created_at')
    return render(request, 'portfolio_admin/blog_comment/list.html', {'comments': comments})

@admin_required
def blog_comment_detail(request, pk):
    comment = get_object_or_404(BlogComment, pk=pk)
    return render(request, 'portfolio_admin/blog_comment/detail.html', {'comment': comment})

@admin_required
@require_POST
def blog_comment_approve(request, pk):
    comment = get_object_or_404(BlogComment, pk=pk)
    comment.is_approved = True
    comment.save()
    return JsonResponse({'status': 'success', 'message': 'Comment approved successfully'})

@admin_required
@require_POST
def blog_comment_delete(request, pk):
    comment = get_object_or_404(BlogComment, pk=pk)
    comment.delete()
    return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully'})

# Award Views
@admin_required
def award_list(request):
    awards = Award.objects.all().order_by('-date_received')
    return render(request, 'portfolio_admin/award/list.html', {'awards': awards})

@admin_required
def award_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Award created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/award/create.html')

@admin_required
def award_update(request, pk):
    award = get_object_or_404(Award, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Award updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/award/update.html', {'award': award})

@admin_required
@require_POST
def award_delete(request, pk):
    award = get_object_or_404(Award, pk=pk)
    award.delete()
    return JsonResponse({'status': 'success', 'message': 'Award deleted successfully'})

# Social Media Views
@admin_required
def social_media_list(request):
    social_medias = SocialMedia.objects.all()
    return render(request, 'portfolio_admin/social_media/list.html', {'social_medias': social_medias})

@admin_required
def social_media_create(request):
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Social Media created successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/social_media/create.html')

@admin_required
def social_media_update(request, pk):
    social_media = get_object_or_404(SocialMedia, pk=pk)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Social Media updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/social_media/update.html', {'social_media': social_media})

@admin_required
@require_POST
def social_media_delete(request, pk):
    social_media = get_object_or_404(SocialMedia, pk=pk)
    social_media.delete()
    return JsonResponse({'status': 'success', 'message': 'Social Media deleted successfully'})

# Portfolio Settings Views
@admin_required
def portfolio_settings(request):
    settings, created = PortfolioSettings.objects.get_or_create(pk=1)
    if request.method == 'POST':
        # Process form data
        response_data = {'status': 'success', 'message': 'Settings updated successfully'}
        return JsonResponse(response_data)
    return render(request, 'portfolio_admin/settings.html', {'settings': settings})
