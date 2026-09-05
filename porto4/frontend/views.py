from django.shortcuts import render
from django.views.generic import TemplateView
from .models import (
    UserProfile, SkillCategory, Skill, Education, Experience,
    ProjectCategory, Technology, Project, Certificate, CertificateCategory,
    Service, SiteSettings, Statistic
)

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get site settings
        try:
            context['site_settings'] = SiteSettings.objects.first()
        except:
            context['site_settings'] = None
        
        # Get skills grouped by category
        skill_categories = SkillCategory.objects.all()
        skills_by_category = {}
        for category in skill_categories:
            skills_by_category[category] = Skill.objects.filter(category=category)
        context['skill_categories'] = skill_categories
        context['skills_by_category'] = skills_by_category
        
        # Get education
        context['education'] = Education.objects.all()
        
        # Get experience
        context['experiences'] = Experience.objects.all()
        
        # Get projects
        context['projects'] = Project.objects.filter(is_featured=True)
        context['project_categories'] = ProjectCategory.objects.all()
        
        # Get certificates grouped by category
        certificate_categories = CertificateCategory.objects.all()
        certificates_by_category = {}
        for category in certificate_categories:
            certificates_by_category[category] = Certificate.objects.filter(category=category, is_featured=True)
        context['certificate_categories'] = certificate_categories
        context['certificates_by_category'] = certificates_by_category
        context['certificates'] = Certificate.objects.filter(is_featured=True)
        
        # Get services
        context['services'] = Service.objects.filter(is_featured=True)
        
        # Get statistics
        context['statistics'] = Statistic.objects.filter(is_featured=True)
        
        return context

def index(request):
    # Get site settings
    try:
        site_settings = SiteSettings.objects.first()
    except:
        site_settings = None
    
    # Get skills grouped by category
    skill_categories = SkillCategory.objects.all()
    skills_by_category = {}
    for category in skill_categories:
        skills_by_category[category] = Skill.objects.filter(category=category)
    
    # Get education
    education = Education.objects.all()
    
    # Get experience
    experiences = Experience.objects.all()
    
    # Get projects
    projects = Project.objects.filter(is_featured=True)
    project_categories = ProjectCategory.objects.all()
    
    # Get certificates
    certificates = Certificate.objects.filter(is_featured=True)
    
    # Get services
    services = Service.objects.filter(is_featured=True)
    
    # Get statistics
    statistics = Statistic.objects.filter(is_featured=True)
    
    context = {
        'site_settings': site_settings,
        'skill_categories': skill_categories,
        'skills_by_category': skills_by_category,
        'education': education,
        'experiences': experiences,
        'projects': projects,
        'project_categories': project_categories,
        'certificates': certificates,
        'services': services,
        'statistics': statistics,
    }
    
    return render(request, 'index.html', context)
