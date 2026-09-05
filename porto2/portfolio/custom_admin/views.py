from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main_app.models import (
    Project, PersonalInfo, Skill, Education, Experience, Certificate, 
    Service, Testimonial, ContactMessage, BlogPost, BlogCategory,
    ProjectCategory, SkillCategory, ProjectImage, SocialMedia
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

# Login view
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('custom_admin:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Username atau password salah')
    
    return render(request, 'custom_admin/login.html')

# Logout view
@login_required
def admin_logout(request):
    logout(request)
    return redirect('custom_admin:login')

# Dashboard view
@login_required
def dashboard(request):
    projects_count = Project.objects.count()
    try:
        personal_info = PersonalInfo.objects.first()
        skills_count = Skill.objects.filter(personal_info=personal_info).count() if personal_info else 0
        education_count = Education.objects.filter(personal_info=personal_info).count() if personal_info else 0
        experience_count = Experience.objects.filter(personal_info=personal_info).count() if personal_info else 0
        certificate_count = Certificate.objects.filter(personal_info=personal_info).count() if personal_info else 0
        message_count = ContactMessage.objects.filter(personal_info=personal_info, status='new').count() if personal_info else 0
        blog_count = BlogPost.objects.filter(personal_info=personal_info).count() if personal_info else 0
    except PersonalInfo.DoesNotExist:
        personal_info = None
        skills_count = 0
        education_count = 0
        experience_count = 0
        certificate_count = 0
        message_count = 0
        blog_count = 0
    
    context = {
        'projects_count': projects_count,
        'skills_count': skills_count,
        'education_count': education_count,
        'experience_count': experience_count,
        'certificate_count': certificate_count,
        'message_count': message_count,
        'blog_count': blog_count,
        'personal_info': personal_info is not None
    }
    
    return render(request, 'custom_admin/dashboard.html', context)

# Project management views
@login_required
def project_list(request):
    projects = Project.objects.all().order_by('-is_featured', 'order', '-date_created')
    return render(request, 'custom_admin/project_list.html', {'projects': projects})

@login_required
def project_add(request):
    # Dapatkan personal_info
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    # Dapatkan kategori proyek
    categories = ProjectCategory.objects.all().order_by('order')
    if not categories.exists():
        messages.error(request, 'Anda harus membuat minimal satu kategori proyek terlebih dahulu')
        return redirect('custom_admin:project_category_add')
    
    # Dapatkan skill untuk teknologi
    skills = Skill.objects.filter(personal_info=personal_info).order_by('name')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        category_id = request.POST.get('category')
        description_short = request.POST.get('description_short')
        description_full = request.POST.get('description_full')
        client = request.POST.get('client')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_ongoing = request.POST.get('is_ongoing') == 'on'
        website_url = request.POST.get('website_url')
        github_url = request.POST.get('github_url')
        thumbnail = request.FILES.get('thumbnail')
        featured_image = request.FILES.get('featured_image')
        model_3d = request.FILES.get('model_3d')
        is_featured = request.POST.get('is_featured') == 'on'
        order = request.POST.get('order', 0)
        technologies = request.POST.getlist('technologies')
        
        if name and slug and category_id and description_short and description_full and start_date and thumbnail:
            try:
                category = ProjectCategory.objects.get(pk=category_id)
                
                # Buat proyek baru
                project = Project.objects.create(
                    personal_info=personal_info,
                    category=category,
                    name=name,
                    slug=slug,
                    description_short=description_short,
                    description_full=description_full,
                    client=client,
                    start_date=start_date,
                    end_date=None if is_ongoing else end_date,
                    is_ongoing=is_ongoing,
                    website_url=website_url,
                    github_url=github_url,
                    thumbnail=thumbnail,
                    featured_image=featured_image,
                    model_3d=model_3d,
                    is_featured=is_featured,
                    order=order
                )
                
                # Tambahkan teknologi
                if technologies:
                    project.technologies.set(technologies)
                
                messages.success(request, 'Proyek berhasil ditambahkan')
                return redirect('custom_admin:project_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Semua field yang wajib harus diisi')
    
    context = {
        'categories': categories,
        'skills': skills
    }
    return render(request, 'custom_admin/project_form.html', context)

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    personal_info = PersonalInfo.objects.first()
    categories = ProjectCategory.objects.all().order_by('order')
    skills = Skill.objects.filter(personal_info=personal_info).order_by('name')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        category_id = request.POST.get('category')
        description_short = request.POST.get('description_short')
        description_full = request.POST.get('description_full')
        client = request.POST.get('client')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_ongoing = request.POST.get('is_ongoing') == 'on'
        website_url = request.POST.get('website_url')
        github_url = request.POST.get('github_url')
        thumbnail = request.FILES.get('thumbnail')
        featured_image = request.FILES.get('featured_image')
        model_3d = request.FILES.get('model_3d')
        is_featured = request.POST.get('is_featured') == 'on'
        order = request.POST.get('order', 0)
        technologies = request.POST.getlist('technologies')
        
        if name and slug and category_id and description_short and description_full and start_date:
            try:
                category = ProjectCategory.objects.get(pk=category_id)
                
                # Update proyek
                project.name = name
                project.slug = slug
                project.category = category
                project.description_short = description_short
                project.description_full = description_full
                project.client = client
                project.start_date = start_date
                project.end_date = None if is_ongoing else end_date
                project.is_ongoing = is_ongoing
                project.website_url = website_url
                project.github_url = github_url
                project.is_featured = is_featured
                project.order = order
                
                if thumbnail:
                    project.thumbnail = thumbnail
                
                if featured_image:
                    project.featured_image = featured_image
                
                if model_3d:
                    project.model_3d = model_3d
                
                project.save()
                
                # Update teknologi
                project.technologies.set(technologies)
                
                messages.success(request, 'Proyek berhasil diupdate')
                return redirect('custom_admin:project_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Semua field yang wajib harus diisi')
    
    context = {
        'project': project,
        'categories': categories,
        'skills': skills,
        'selected_technologies': [tech.id for tech in project.technologies.all()]
    }
    return render(request, 'custom_admin/project_form.html', context)

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Proyek berhasil dihapus')
        return redirect('custom_admin:project_list')
    
    return render(request, 'custom_admin/project_confirm_delete.html', {'project': project})

@login_required
def project_image_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    images = project.images.all().order_by('order')
    
    return render(request, 'custom_admin/project_image_list.html', {
        'project': project,
        'images': images
    })

@login_required
def project_image_add(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        description = request.POST.get('description')
        order = request.POST.get('order', 0)
        
        if image:
            ProjectImage.objects.create(
                project=project,
                image=image,
                title=title,
                description=description,
                order=order
            )
            messages.success(request, 'Gambar proyek berhasil ditambahkan')
            return redirect('custom_admin:project_image_list', project_id=project.id)
        else:
            messages.error(request, 'Gambar harus diupload')
    
    return render(request, 'custom_admin/project_image_form.html', {'project': project})

@login_required
def project_image_edit(request, image_id):
    image = get_object_or_404(ProjectImage, pk=image_id)
    project = image.project
    
    if request.method == 'POST':
        new_image = request.FILES.get('image')
        title = request.POST.get('title')
        description = request.POST.get('description')
        order = request.POST.get('order', 0)
        
        image.title = title
        image.description = description
        image.order = order
        
        if new_image:
            image.image = new_image
        
        image.save()
        messages.success(request, 'Gambar proyek berhasil diupdate')
        return redirect('custom_admin:project_image_list', project_id=project.id)
    
    return render(request, 'custom_admin/project_image_form.html', {
        'project': project,
        'image': image
    })

@login_required
def project_image_delete(request, image_id):
    image = get_object_or_404(ProjectImage, pk=image_id)
    project = image.project
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Gambar proyek berhasil dihapus')
        return redirect('custom_admin:project_image_list', project_id=project.id)
    
    return render(request, 'custom_admin/project_image_confirm_delete.html', {
        'project': project,
        'image': image
    })

@login_required
def project_category_list(request):
    categories = ProjectCategory.objects.all().order_by('order')
    return render(request, 'custom_admin/project_category_list.html', {'categories': categories})

@login_required
def project_category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if name:
            ProjectCategory.objects.create(
                name=name,
                description=description,
                icon_class=icon_class,
                order=order
            )
            messages.success(request, 'Kategori proyek berhasil ditambahkan')
            return redirect('custom_admin:project_category_list')
        else:
            messages.error(request, 'Nama kategori harus diisi')
    
    return render(request, 'custom_admin/project_category_form.html')

@login_required
def project_category_edit(request, pk):
    category = get_object_or_404(ProjectCategory, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if name:
            category.name = name
            category.description = description
            category.icon_class = icon_class
            category.order = order
            category.save()
            
            messages.success(request, 'Kategori proyek berhasil diupdate')
            return redirect('custom_admin:project_category_list')
        else:
            messages.error(request, 'Nama kategori harus diisi')
    
    return render(request, 'custom_admin/project_category_form.html', {'category': category})

@login_required
def project_category_delete(request, pk):
    category = get_object_or_404(ProjectCategory, pk=pk)
    
    # Periksa apakah ada proyek yang menggunakan kategori ini
    if Project.objects.filter(category=category).exists():
        messages.error(request, 'Kategori ini tidak dapat dihapus karena sedang digunakan oleh proyek')
        return redirect('custom_admin:project_category_list')
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori proyek berhasil dihapus')
        return redirect('custom_admin:project_category_list')
    
    return render(request, 'custom_admin/project_category_confirm_delete.html', {'category': category})

# Personal Info management view
@login_required
def personal_info_edit(request):
    personal_info = PersonalInfo.objects.first()
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        job_title = request.POST.get('job_title')
        bio_short = request.POST.get('bio_short')
        bio_full = request.POST.get('bio_full')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')
        cv_file = request.FILES.get('cv_file')
        
        if full_name and job_title and bio_short and bio_full and email:
            if personal_info:
                personal_info.full_name = full_name
                personal_info.job_title = job_title
                personal_info.bio_short = bio_short
                personal_info.bio_full = bio_full
                personal_info.birth_date = birth_date
                personal_info.address = address
                personal_info.phone = phone
                personal_info.email = email
                
                if profile_image:
                    personal_info.profile_image = profile_image
                
                if cv_file:
                    personal_info.cv_file = cv_file
                
                personal_info.save()
            else:
                personal_info = PersonalInfo.objects.create(
                    full_name=full_name,
                    job_title=job_title,
                    bio_short=bio_short,
                    bio_full=bio_full,
                    birth_date=birth_date,
                    address=address,
                    phone=phone,
                    email=email,
                    profile_image=profile_image,
                    cv_file=cv_file
                )
            
            messages.success(request, 'Informasi Personal berhasil diupdate')
            return redirect('custom_admin:dashboard')
        else:
            messages.error(request, 'Semua field yang wajib harus diisi')
    
    return render(request, 'custom_admin/personal_info_form.html', {'personal_info': personal_info})

# Social Media management views
@login_required
def social_media_list(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    social_media = SocialMedia.objects.filter(personal_info=personal_info).order_by('order')
    return render(request, 'custom_admin/social_media_list.html', {'social_media': social_media})

@login_required
def social_media_add(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    if request.method == 'POST':
        platform = request.POST.get('platform')
        url = request.POST.get('url')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if platform and url and icon_class:
            SocialMedia.objects.create(
                personal_info=personal_info,
                platform=platform,
                url=url,
                icon_class=icon_class,
                order=order
            )
            messages.success(request, 'Social Media berhasil ditambahkan')
            return redirect('custom_admin:social_media_list')
        else:
            messages.error(request, 'Semua field harus diisi')
    
    return render(request, 'custom_admin/social_media_form.html')

@login_required
def social_media_edit(request, pk):
    social_media = get_object_or_404(SocialMedia, pk=pk)
    
    if request.method == 'POST':
        platform = request.POST.get('platform')
        url = request.POST.get('url')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if platform and url and icon_class:
            social_media.platform = platform
            social_media.url = url
            social_media.icon_class = icon_class
            social_media.order = order
            social_media.save()
            
            messages.success(request, 'Social Media berhasil diupdate')
            return redirect('custom_admin:social_media_list')
        else:
            messages.error(request, 'Semua field harus diisi')
    
    return render(request, 'custom_admin/social_media_form.html', {'social_media': social_media})

@login_required
def social_media_delete(request, pk):
    social_media = get_object_or_404(SocialMedia, pk=pk)
    
    if request.method == 'POST':
        social_media.delete()
        messages.success(request, 'Social Media berhasil dihapus')
        return redirect('custom_admin:social_media_list')
    
    return render(request, 'custom_admin/social_media_confirm_delete.html', {'social_media': social_media})

# Skill Category management views
@login_required
def skill_category_list(request):
    categories = SkillCategory.objects.all().order_by('order')
    return render(request, 'custom_admin/skill_category_list.html', {'categories': categories})

@login_required
def skill_category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if name:
            SkillCategory.objects.create(
                name=name,
                description=description,
                icon_class=icon_class,
                order=order
            )
            messages.success(request, 'Kategori skill berhasil ditambahkan')
            return redirect('custom_admin:skill_category_list')
        else:
            messages.error(request, 'Nama kategori harus diisi')
    
    return render(request, 'custom_admin/skill_category_form.html')

@login_required
def skill_category_edit(request, pk):
    category = get_object_or_404(SkillCategory, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if name:
            category.name = name
            category.description = description
            category.icon_class = icon_class
            category.order = order
            category.save()
            
            messages.success(request, 'Kategori skill berhasil diupdate')
            return redirect('custom_admin:skill_category_list')
        else:
            messages.error(request, 'Nama kategori harus diisi')
    
    return render(request, 'custom_admin/skill_category_form.html', {'category': category})

@login_required
def skill_category_delete(request, pk):
    category = get_object_or_404(SkillCategory, pk=pk)
    
    # Periksa apakah ada skill yang menggunakan kategori ini
    if Skill.objects.filter(category=category).exists():
        messages.error(request, 'Kategori ini tidak dapat dihapus karena sedang digunakan oleh skill')
        return redirect('custom_admin:skill_category_list')
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori skill berhasil dihapus')
        return redirect('custom_admin:skill_category_list')
    
    return render(request, 'custom_admin/skill_category_confirm_delete.html', {'category': category})

# Skills management views
@login_required
def skill_list(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    skills = Skill.objects.filter(personal_info=personal_info).order_by('category__order', 'order')
    return render(request, 'custom_admin/skill_list.html', {'skills': skills})

@login_required
def skill_add(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    # Dapatkan kategori skill
    categories = SkillCategory.objects.all().order_by('order')
    if not categories.exists():
        messages.error(request, 'Anda harus membuat minimal satu kategori skill terlebih dahulu')
        return redirect('custom_admin:skill_category_add')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        percentage = request.POST.get('percentage')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if name and category_id and percentage:
            try:
                category = SkillCategory.objects.get(pk=category_id)
                percentage = int(percentage)
                if 0 <= percentage <= 100:
                    Skill.objects.create(
                        personal_info=personal_info,
                        category=category,
                        name=name,
                        percentage=percentage,
                        icon_class=icon_class,
                        order=order
                    )
                    messages.success(request, 'Skill berhasil ditambahkan')
                    return redirect('custom_admin:skill_list')
                else:
                    messages.error(request, 'Persentase harus antara 0-100')
            except SkillCategory.DoesNotExist:
                messages.error(request, 'Kategori skill tidak ditemukan')
            except ValueError:
                messages.error(request, 'Persentase harus berupa angka')
        else:
            messages.error(request, 'Nama, kategori, dan persentase harus diisi')
    
    context = {
        'categories': categories
    }
    return render(request, 'custom_admin/skill_form.html', context)

@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    categories = SkillCategory.objects.all().order_by('order')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        percentage = request.POST.get('percentage')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if name and category_id and percentage:
            try:
                category = SkillCategory.objects.get(pk=category_id)
                percentage = int(percentage)
                if 0 <= percentage <= 100:
                    skill.name = name
                    skill.category = category
                    skill.percentage = percentage
                    skill.icon_class = icon_class
                    skill.order = order
                    skill.save()
                    
                    messages.success(request, 'Skill berhasil diupdate')
                    return redirect('custom_admin:skill_list')
                else:
                    messages.error(request, 'Persentase harus antara 0-100')
            except SkillCategory.DoesNotExist:
                messages.error(request, 'Kategori skill tidak ditemukan')
            except ValueError:
                messages.error(request, 'Persentase harus berupa angka')
        else:
            messages.error(request, 'Nama, kategori, dan persentase harus diisi')
    
    context = {
        'skill': skill,
        'categories': categories
    }
    return render(request, 'custom_admin/skill_form.html', context)

@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    
    # Periksa apakah skill ini digunakan oleh proyek
    if skill.projects.exists():
        messages.error(request, 'Skill ini tidak dapat dihapus karena sedang digunakan oleh proyek')
        return redirect('custom_admin:skill_list')
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill berhasil dihapus')
        return redirect('custom_admin:skill_list')
    
    return render(request, 'custom_admin/skill_confirm_delete.html', {'skill': skill})

# Education management views
@login_required
def education_list(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    educations = Education.objects.filter(personal_info=personal_info).order_by('-end_date', '-start_date')
    return render(request, 'custom_admin/education_list.html', {'educations': educations})

@login_required
def education_add(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    if request.method == 'POST':
        institution = request.POST.get('institution')
        degree = request.POST.get('degree')
        field_of_study = request.POST.get('field_of_study')
        location = request.POST.get('location')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_ongoing = request.POST.get('is_ongoing') == 'on'
        logo = request.FILES.get('logo')
        
        if institution and degree and start_date:
            try:
                Education.objects.create(
                    personal_info=personal_info,
                    institution=institution,
                    degree=degree,
                    field_of_study=field_of_study,
                    location=location,
                    description=description,
                    start_date=start_date,
                    end_date=None if is_ongoing else end_date,
                    is_ongoing=is_ongoing,
                    logo=logo
                )
                messages.success(request, 'Pendidikan berhasil ditambahkan')
                return redirect('custom_admin:education_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Institusi, gelar, dan tanggal mulai harus diisi')
    
    return render(request, 'custom_admin/education_form.html')

@login_required
def education_edit(request, pk):
    education = get_object_or_404(Education, pk=pk)
    
    if request.method == 'POST':
        institution = request.POST.get('institution')
        degree = request.POST.get('degree')
        field_of_study = request.POST.get('field_of_study')
        location = request.POST.get('location')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_ongoing = request.POST.get('is_ongoing') == 'on'
        logo = request.FILES.get('logo')
        
        if institution and degree and start_date:
            try:
                education.institution = institution
                education.degree = degree
                education.field_of_study = field_of_study
                education.location = location
                education.description = description
                education.start_date = start_date
                education.end_date = None if is_ongoing else end_date
                education.is_ongoing = is_ongoing
                
                if logo:
                    education.logo = logo
                
                education.save()
                messages.success(request, 'Pendidikan berhasil diupdate')
                return redirect('custom_admin:education_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Institusi, gelar, dan tanggal mulai harus diisi')
    
    return render(request, 'custom_admin/education_form.html', {'education': education})

@login_required
def education_delete(request, pk):
    education = get_object_or_404(Education, pk=pk)
    
    if request.method == 'POST':
        education.delete()
        messages.success(request, 'Pendidikan berhasil dihapus')
        return redirect('custom_admin:education_list')
    
    return render(request, 'custom_admin/education_confirm_delete.html', {'education': education})

# Experience management views
@login_required
def experience_list(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    experiences = Experience.objects.filter(personal_info=personal_info).order_by('-end_date', '-start_date')
    return render(request, 'custom_admin/experience_list.html', {'experiences': experiences})

@login_required
def experience_add(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    if request.method == 'POST':
        company = request.POST.get('company')
        position = request.POST.get('position')
        location = request.POST.get('location')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_ongoing = request.POST.get('is_ongoing') == 'on'
        company_logo = request.FILES.get('company_logo')
        
        if company and position and start_date:
            try:
                Experience.objects.create(
                    personal_info=personal_info,
                    company=company,
                    position=position,
                    location=location,
                    description=description,
                    start_date=start_date,
                    end_date=None if is_ongoing else end_date,
                    is_ongoing=is_ongoing,
                    company_logo=company_logo
                )
                messages.success(request, 'Pengalaman kerja berhasil ditambahkan')
                return redirect('custom_admin:experience_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Perusahaan, posisi, dan tanggal mulai harus diisi')
    
    return render(request, 'custom_admin/experience_form.html')

@login_required
def experience_edit(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    
    if request.method == 'POST':
        company = request.POST.get('company')
        position = request.POST.get('position')
        location = request.POST.get('location')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_ongoing = request.POST.get('is_ongoing') == 'on'
        company_logo = request.FILES.get('company_logo')
        
        if company and position and start_date:
            try:
                experience.company = company
                experience.position = position
                experience.location = location
                experience.description = description
                experience.start_date = start_date
                experience.end_date = None if is_ongoing else end_date
                experience.is_ongoing = is_ongoing
                
                if company_logo:
                    experience.company_logo = company_logo
                
                experience.save()
                messages.success(request, 'Pengalaman kerja berhasil diupdate')
                return redirect('custom_admin:experience_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Perusahaan, posisi, dan tanggal mulai harus diisi')
    
    return render(request, 'custom_admin/experience_form.html', {'experience': experience})

@login_required
def experience_delete(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    
    if request.method == 'POST':
        experience.delete()
        messages.success(request, 'Pengalaman kerja berhasil dihapus')
        return redirect('custom_admin:experience_list')
    
    return render(request, 'custom_admin/experience_confirm_delete.html', {'experience': experience})

# Certificate management views
@login_required
def certificate_list(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    certificates = Certificate.objects.filter(personal_info=personal_info).order_by('-issue_date')
    return render(request, 'custom_admin/certificate_list.html', {'certificates': certificates})

@login_required
def certificate_add(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        organization = request.POST.get('organization')
        issue_date = request.POST.get('issue_date')
        expiry_date = request.POST.get('expiry_date')
        credential_id = request.POST.get('credential_id')
        credential_url = request.POST.get('credential_url')
        description = request.POST.get('description')
        certificate_image = request.FILES.get('certificate_image')
        
        if name and organization and issue_date:
            try:
                Certificate.objects.create(
                    personal_info=personal_info,
                    name=name,
                    organization=organization,
                    issue_date=issue_date,
                    expiry_date=expiry_date,
                    credential_id=credential_id,
                    credential_url=credential_url,
                    description=description,
                    certificate_image=certificate_image
                )
                messages.success(request, 'Sertifikat berhasil ditambahkan')
                return redirect('custom_admin:certificate_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Nama, organisasi, dan tanggal terbit harus diisi')
    
    return render(request, 'custom_admin/certificate_form.html')

@login_required
def certificate_edit(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        organization = request.POST.get('organization')
        issue_date = request.POST.get('issue_date')
        expiry_date = request.POST.get('expiry_date')
        credential_id = request.POST.get('credential_id')
        credential_url = request.POST.get('credential_url')
        description = request.POST.get('description')
        certificate_image = request.FILES.get('certificate_image')
        
        if name and organization and issue_date:
            try:
                certificate.name = name
                certificate.organization = organization
                certificate.issue_date = issue_date
                certificate.expiry_date = expiry_date
                certificate.credential_id = credential_id
                certificate.credential_url = credential_url
                certificate.description = description
                
                if certificate_image:
                    certificate.certificate_image = certificate_image
                
                certificate.save()
                messages.success(request, 'Sertifikat berhasil diupdate')
                return redirect('custom_admin:certificate_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Nama, organisasi, dan tanggal terbit harus diisi')
    
    return render(request, 'custom_admin/certificate_form.html', {'certificate': certificate})

@login_required
def certificate_delete(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    
    if request.method == 'POST':
        certificate.delete()
        messages.success(request, 'Sertifikat berhasil dihapus')
        return redirect('custom_admin:certificate_list')
    
    return render(request, 'custom_admin/certificate_confirm_delete.html', {'certificate': certificate})

# Service management views
@login_required
def service_list(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    services = Service.objects.filter(personal_info=personal_info).order_by('order')
    return render(request, 'custom_admin/service_list.html', {'services': services})

@login_required
def service_add(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if title and description:
            try:
                Service.objects.create(
                    personal_info=personal_info,
                    title=title,
                    description=description,
                    icon_class=icon_class,
                    order=order
                )
                messages.success(request, 'Layanan berhasil ditambahkan')
                return redirect('custom_admin:service_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Judul dan deskripsi harus diisi')
    
    return render(request, 'custom_admin/service_form.html')

@login_required
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        icon_class = request.POST.get('icon_class')
        order = request.POST.get('order', 0)
        
        if title and description:
            try:
                service.title = title
                service.description = description
                service.icon_class = icon_class
                service.order = order
                service.save()
                
                messages.success(request, 'Layanan berhasil diupdate')
                return redirect('custom_admin:service_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Judul dan deskripsi harus diisi')
    
    return render(request, 'custom_admin/service_form.html', {'service': service})

@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Layanan berhasil dihapus')
        return redirect('custom_admin:service_list')
    
    return render(request, 'custom_admin/service_confirm_delete.html', {'service': service})

# Testimonial management views
@login_required
def testimonial_list(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    testimonials = Testimonial.objects.filter(personal_info=personal_info).order_by('order')
    return render(request, 'custom_admin/testimonial_list.html', {'testimonials': testimonials})

@login_required
def testimonial_add(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        company = request.POST.get('company')
        content = request.POST.get('content')
        avatar = request.FILES.get('avatar')
        order = request.POST.get('order', 0)
        
        if name and content:
            try:
                Testimonial.objects.create(
                    personal_info=personal_info,
                    name=name,
                    position=position,
                    company=company,
                    content=content,
                    avatar=avatar,
                    order=order
                )
                messages.success(request, 'Testimonial berhasil ditambahkan')
                return redirect('custom_admin:testimonial_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Nama dan konten testimonial harus diisi')
    
    return render(request, 'custom_admin/testimonial_form.html')

@login_required
def testimonial_edit(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        company = request.POST.get('company')
        content = request.POST.get('content')
        avatar = request.FILES.get('avatar')
        order = request.POST.get('order', 0)
        
        if name and content:
            try:
                testimonial.name = name
                testimonial.position = position
                testimonial.company = company
                testimonial.content = content
                testimonial.order = order
                
                if avatar:
                    testimonial.avatar = avatar
                
                testimonial.save()
                messages.success(request, 'Testimonial berhasil diupdate')
                return redirect('custom_admin:testimonial_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Nama dan konten testimonial harus diisi')
    
    return render(request, 'custom_admin/testimonial_form.html', {'testimonial': testimonial})

@login_required
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial berhasil dihapus')
        return redirect('custom_admin:testimonial_list')
    
    return render(request, 'custom_admin/testimonial_confirm_delete.html', {'testimonial': testimonial})

# Contact Message management views
@login_required
def contact_message_list(request):
    messages_list = ContactMessage.objects.all().order_by('-date_sent')
    return render(request, 'custom_admin/contact_message_list.html', {'messages': messages_list})

@login_required
def contact_message_view(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    
    # Mark as read if not already
    if not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'custom_admin/contact_message_view.html', {'message': message})

@login_required
def contact_message_delete(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Pesan berhasil dihapus')
        return redirect('custom_admin:contact_message_list')
    
    return render(request, 'custom_admin/contact_message_confirm_delete.html', {'message': message})

# Blog Category management views
@login_required
def blog_category_list(request):
    categories = BlogCategory.objects.all().order_by('name')
    return render(request, 'custom_admin/blog_category_list.html', {'categories': categories})

@login_required
def blog_category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            try:
                BlogCategory.objects.create(
                    name=name,
                    description=description
                )
                messages.success(request, 'Kategori blog berhasil ditambahkan')
                return redirect('custom_admin:blog_category_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Nama kategori harus diisi')
    
    return render(request, 'custom_admin/blog_category_form.html')

@login_required
def blog_category_edit(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            try:
                category.name = name
                category.description = description
                category.save()
                
                messages.success(request, 'Kategori blog berhasil diupdate')
                return redirect('custom_admin:blog_category_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Nama kategori harus diisi')
    
    return render(request, 'custom_admin/blog_category_form.html', {'category': category})

@login_required
def blog_category_delete(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    
    # Periksa apakah ada blog post yang menggunakan kategori ini
    if BlogPost.objects.filter(category=category).exists():
        messages.error(request, 'Kategori ini tidak dapat dihapus karena sedang digunakan oleh blog post')
        return redirect('custom_admin:blog_category_list')
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori blog berhasil dihapus')
        return redirect('custom_admin:blog_category_list')
    
    return render(request, 'custom_admin/blog_category_confirm_delete.html', {'category': category})

# Blog Post management views
@login_required
def blog_post_list(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    posts = BlogPost.objects.filter(author=personal_info).order_by('-date_published')
    return render(request, 'custom_admin/blog_post_list.html', {'posts': posts})

@login_required
def blog_post_add(request):
    personal_info = PersonalInfo.objects.first()
    if not personal_info:
        messages.error(request, 'Anda harus membuat profil Personal Information terlebih dahulu')
        return redirect('custom_admin:personal_info_edit')
    
    # Dapatkan kategori blog
    categories = BlogCategory.objects.all().order_by('name')
    if not categories.exists():
        messages.error(request, 'Anda harus membuat minimal satu kategori blog terlebih dahulu')
        return redirect('custom_admin:blog_category_add')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        category_id = request.POST.get('category')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt')
        featured_image = request.FILES.get('featured_image')
        is_published = request.POST.get('is_published') == 'on'
        date_published = request.POST.get('date_published')
        
        if title and slug and category_id and content:
            try:
                category = BlogCategory.objects.get(pk=category_id)
                
                BlogPost.objects.create(
                    author=personal_info,
                    category=category,
                    title=title,
                    slug=slug,
                    content=content,
                    excerpt=excerpt,
                    featured_image=featured_image,
                    is_published=is_published,
                    date_published=date_published if is_published and date_published else None
                )
                messages.success(request, 'Blog post berhasil ditambahkan')
                return redirect('custom_admin:blog_post_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Judul, slug, kategori, dan konten harus diisi')
    
    context = {
        'categories': categories
    }
    return render(request, 'custom_admin/blog_post_form.html', context)

@login_required
def blog_post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    categories = BlogCategory.objects.all().order_by('name')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        category_id = request.POST.get('category')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt')
        featured_image = request.FILES.get('featured_image')
        is_published = request.POST.get('is_published') == 'on'
        date_published = request.POST.get('date_published')
        
        if title and slug and category_id and content:
            try:
                category = BlogCategory.objects.get(pk=category_id)
                
                post.title = title
                post.slug = slug
                post.category = category
                post.content = content
                post.excerpt = excerpt
                post.is_published = is_published
                post.date_published = date_published if is_published and date_published else None
                
                if featured_image:
                    post.featured_image = featured_image
                
                post.save()
                messages.success(request, 'Blog post berhasil diupdate')
                return redirect('custom_admin:blog_post_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Judul, slug, kategori, dan konten harus diisi')
    
    context = {
        'post': post,
        'categories': categories
    }
    return render(request, 'custom_admin/blog_post_form.html', context)

@login_required
def blog_post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post berhasil dihapus')
        return redirect('custom_admin:blog_post_list')
    
    return render(request, 'custom_admin/blog_post_confirm_delete.html', {'post': post})
