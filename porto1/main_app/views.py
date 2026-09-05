from django.shortcuts import render
from custom_admin.models import (
    Profile, About, Education, Skill, Project, Experience, 
    Certificate, Contact, Service, Testimonial, Blog, Award, 
    SocialMedia, PortfolioSettings
)

def home(request):
    """Halaman beranda portofolio dengan tema galaxy"""
    try:
        profile = Profile.objects.filter(is_active=True).first()
        about = About.objects.filter(is_active=True).first() if profile else None
        skills = Skill.objects.filter(is_active=True, profile=profile).order_by('-percentage')[:8] if profile else []
        featured_projects = Project.objects.filter(is_active=True, is_featured=True, profile=profile).order_by('-created_at')[:6] if profile else []
        all_projects = Project.objects.filter(is_active=True, profile=profile).order_by('-created_at') if profile else []
        services = Service.objects.filter(is_active=True, profile=profile).order_by('title')[:6] if profile else []
        testimonials = Testimonial.objects.filter(is_active=True, is_featured=True, profile=profile).order_by('-rating')[:3] if profile else []
        experiences = Experience.objects.filter(is_active=True, profile=profile).order_by('-start_date')[:3] if profile else []
        education = Education.objects.filter(is_active=True, profile=profile).order_by('-end_date', '-start_date')[:3] if profile else []
        certificates = Certificate.objects.filter(is_active=True, is_featured=True, profile=profile).order_by('-issue_date')[:4] if profile else []
        awards = Award.objects.filter(is_active=True, is_featured=True, profile=profile).order_by('-date_received')[:3] if profile else []
        social_media = SocialMedia.objects.filter(is_active=True, profile=profile).order_by('platform') if profile else []
        settings = PortfolioSettings.objects.filter(profile=profile).first() if profile else None
    except Exception as e:
        profile = None
        about = None
        skills = []
        featured_projects = []
        all_projects = []
        services = []
        testimonials = []
        experiences = []
        education = []
        certificates = []
        awards = []
        social_media = []
        settings = None
    
    context = {
        'profile': profile,
        'about': about,
        'skills': skills,
        'featured_projects': featured_projects,
        'projects': all_projects,
        'services': services,
        'testimonials': testimonials,
        'experiences': experiences,
        'education': education,
        'certificates': certificates,
        'awards': awards,
        'social_media': social_media,
        'settings': settings,
        'page_title': 'Beranda - Portofolio Galaxy',
        'is_home': True,
    }
    return render(request, 'main_app/home.html', context)

def contact(request):
    """Halaman kontak untuk form submission"""
    try:
        profile = Profile.objects.filter(is_active=True).first()
        social_media = SocialMedia.objects.filter(is_active=True, profile=profile).order_by('platform') if profile else None
        settings = PortfolioSettings.objects.filter(profile=profile).first() if profile else None
    except Exception as e:
        profile = None
        social_media = []
        settings = None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            try:
                Contact.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                return render(request, 'main_app/home.html', {
                    'success_message': 'Pesan Anda telah berhasil dikirim! Saya akan segera menghubungi Anda.',
                    'profile': profile,
                    'social_media': social_media,
                    'settings': settings,
                    'page_title': 'Beranda - Portofolio Galaxy',
                })
            except Exception as e:
                return render(request, 'main_app/home.html', {
                    'error_message': 'Terjadi kesalahan saat mengirim pesan. Silakan coba lagi.',
                    'profile': profile,
                    'social_media': social_media,
                    'settings': settings,
                    'page_title': 'Beranda - Portofolio Galaxy',
                })
        else:
            return render(request, 'main_app/home.html', {
                'error_message': 'Mohon lengkapi semua field yang diperlukan.',
                'profile': profile,
                'social_media': social_media,
                'settings': settings,
                'page_title': 'Beranda - Portofolio Galaxy',
            })
    
    return render(request, 'main_app/home.html', {
        'profile': profile,
        'social_media': social_media,
        'settings': settings,
        'page_title': 'Beranda - Portofolio Galaxy',
    })
