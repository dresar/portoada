from django.shortcuts import render, get_object_or_404
from .models import Project, PersonalInfo, Skill, Education, Experience, Certificate, Service, Testimonial, BlogPost, ProjectCategory, BlogCategory, SkillCategory, SocialMedia

def home(request):
    """Home page view for single page application"""
    # Ambil informasi personal
    personal_info = PersonalInfo.objects.first()
    
    # Ambil proyek yang ditandai sebagai featured
    featured_projects = Project.objects.filter(is_featured=True).order_by('order', '-date_created')[:6] if personal_info else []
    
    # Ambil skill categories dan skills
    skill_categories = SkillCategory.objects.all().order_by('order') if personal_info else []
    
    # Ambil testimonial yang ditandai sebagai featured
    featured_testimonials = Testimonial.objects.filter(is_featured=True).order_by('order')[:3] if personal_info else []
    
    # Ambil layanan yang ditandai sebagai featured
    featured_services = Service.objects.filter(is_featured=True).order_by('order')[:4] if personal_info else []
    
    # Ambil semua proyek untuk section projects
    all_projects = Project.objects.all().order_by('-is_featured', 'order', '-end_date', '-start_date')
    
    # Ambil semua kategori proyek
    project_categories = ProjectCategory.objects.all().order_by('order')
    
    # Ambil semua blog post untuk section blog
    blog_posts = BlogPost.objects.filter(status='published').order_by('-date_published')[:3]
    
    # Ambil semua kategori blog
    blog_categories = BlogCategory.objects.all()
    
    # Ambil education yang ditandai sebagai featured
    featured_education = Education.objects.filter(is_current=False).order_by('-end_date', '-start_date')[:3] if personal_info else []
    
    # Ambil experience yang ditandai sebagai featured
    featured_experiences = Experience.objects.filter(is_featured=True).order_by('-is_current', '-end_date', '-start_date')[:3] if personal_info else []
    
    # Ambil certificates yang ditandai sebagai featured
    featured_certificates = Certificate.objects.filter(is_featured=True).order_by('-issue_date')[:3] if personal_info else []
    
    # Ambil social media
    social_media = SocialMedia.objects.all() if personal_info else []
    
    context = {
        'personal_info': personal_info,
        'featured_projects': featured_projects,
        'skill_categories': skill_categories,
        'featured_testimonials': featured_testimonials,
        'featured_services': featured_services,
        'all_projects': all_projects,
        'project_categories': project_categories,
        'blog_posts': blog_posts,
        'blog_categories': blog_categories,
        'featured_education': featured_education,
        'featured_experiences': featured_experiences,
        'featured_certificates': featured_certificates,
        'social_media': social_media,
    }
    return render(request, 'main_app/home.html', context)

def project_detail(request, slug):
    """Project detail view for single page application"""
    project = get_object_or_404(Project, slug=slug)
    project_images = project.images.all().order_by('order')
    related_projects = Project.objects.filter(category=project.category).exclude(pk=project.pk)[:3]
    context = {
        'project': project,
        'project_images': project_images,
        'related_projects': related_projects
    }
    return render(request, 'main_app/project_detail.html', context)

def blog_detail(request, slug):
    """Blog detail view for single page application"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    post.view_count += 1
    post.save()
    related_posts = BlogPost.objects.filter(status='published').exclude(pk=post.pk)[:3]
    context = {
        'post': post,
        'related_posts': related_posts
    }
    return render(request, 'main_app/blog_detail.html', context)

def about(request):
    return home(request)

def projects(request):
    return home(request)

def contact(request):
    return home(request)

def blog(request):
    return home(request)
