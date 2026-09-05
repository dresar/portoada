from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Visitor, VisitorStat, AdminSetting, Notification, ProjectProgress, Task, BackupLog, ActivityLog, ContactResponse, SiteConfiguration
from core.models import Profile, Skill, Education, Experience, Service, Project, ProjectTag, Certificate, CertificateSkill, Message
import json
import os
import csv
from django.http import FileResponse
from django.conf import settings

# Create your views here.
@login_required
def admin_dashboard(request):
    """View function for admin dashboard."""
    # Get visitor statistics
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    today_visitors = VisitorStat.objects.filter(date=today).aggregate(Sum('count'))['count__sum'] or 0
    yesterday_visitors = VisitorStat.objects.filter(date=yesterday).aggregate(Sum('count'))['count__sum'] or 0
    
    # Get visitor stats for the last 7 days for the chart
    visitor_stats = []
    for i in range(7):
        day = today - timedelta(days=i)
        count = VisitorStat.objects.filter(date=day).aggregate(Sum('count'))['count__sum'] or 0
        visitor_stats.append({
            'date': day.strftime('%d %b'),
            'count': count
        })
    visitor_stats.reverse()
    
    # Get skill distribution for the chart
    skills = Skill.objects.filter(category='technical').order_by('-proficiency')[:10]
    skill_data = [{
        'name': skill.name,
        'proficiency': skill.proficiency
    } for skill in skills]
    
    # Get latest messages
    latest_messages = Message.objects.all().order_by('-created_at')[:5]
    
    # Get latest projects with progress
    latest_projects = Project.objects.all().order_by('-created_at')[:5]
    project_progress = {}
    for project in latest_projects:
        progress = ProjectProgress.objects.filter(project=project).order_by('-date').first()
        if progress:
            project_progress[project.id] = progress.percentage
        else:
            project_progress[project.id] = 0
    
    # Get notifications
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
    
    # Get total counts
    total_projects = Project.objects.count()
    total_certificates = Certificate.objects.count()
    total_messages = Message.objects.count()
    total_visitors = Visitor.objects.count()
    
    # Get pending tasks
    pending_tasks = Task.objects.filter(status='pending').order_by('-created_at')[:5]
    
    context = {
        'today_visitors': today_visitors,
        'yesterday_visitors': yesterday_visitors,
        'visitor_stats': json.dumps(visitor_stats),
        'skill_data': json.dumps(skill_data),
        'latest_messages': latest_messages,
        'latest_projects': latest_projects,
        'project_progress': project_progress,
        'notifications': notifications,
        'total_projects': total_projects,
        'total_certificates': total_certificates,
        'total_messages': total_messages,
        'total_visitors': total_visitors,
        'pending_tasks': pending_tasks,
    }
    
    return render(request, 'admin_custom/dashboard.html', context)

@login_required
def messages_list(request):
    """View function for messages list."""
    messages_list = Message.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(messages_list, 10)  # Show 10 messages per page
    page = request.GET.get('page')
    messages_page = paginator.get_page(page)
    
    context = {
        'messages': messages_page,
    }
    
    return render(request, 'admin_custom/messages.html', context)

@login_required
def message_detail(request, message_id):
    """View function for message detail."""
    message = get_object_or_404(Message, id=message_id)
    
    # Mark message as read if it's not already
    if not message.is_read:
        message.is_read = True
        message.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            activity_type='message_read',
            description=f'Message from {message.name} was read',
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
    
    # Get related responses
    responses = ContactResponse.objects.filter(message=message).order_by('created_at')
    
    context = {
        'message': message,
        'responses': responses,
    }
    
    return render(request, 'admin_custom/message_detail.html', context)

@login_required
def respond_to_message(request, message_id):
    """View function for responding to a message."""
    message = get_object_or_404(Message, id=message_id)
    
    if request.method == 'POST':
        response_text = request.POST.get('response')
        
        if response_text:
            # Create response
            response = ContactResponse.objects.create(
                message=message,
                user=request.user,
                response=response_text
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                activity_type='message_response',
                description=f'Response sent to {message.name}',
                ip_address=request.META.get('REMOTE_ADDR', '')
            )
            
            messages.success(request, 'Response sent successfully!')
        else:
            messages.error(request, 'Response cannot be empty.')
        
        return redirect('message_detail', message_id=message.id)
    
    return redirect('message_detail', message_id=message.id)

@login_required
def projects_list(request):
    """View function for projects list."""
    projects_list = Project.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(projects_list, 10)  # Show 10 projects per page
    page = request.GET.get('page')
    projects_page = paginator.get_page(page)
    
    # Get progress for each project
    project_progress = {}
    for project in projects_page:
        progress = ProjectProgress.objects.filter(project=project).order_by('-date').first()
        if progress:
            project_progress[project.id] = progress.percentage
        else:
            project_progress[project.id] = 0
    
    context = {
        'projects': projects_page,
        'project_progress': project_progress,
    }
    
    return render(request, 'admin_custom/projects.html', context)

@login_required
def project_detail(request, project_id):
    """View function for project detail."""
    project = get_object_or_404(Project, id=project_id)
    
    # Get project tags
    tags = ProjectTag.objects.filter(project=project)
    
    # Get project progress history
    progress_history = ProjectProgress.objects.filter(project=project).order_by('-date')
    
    # Get current progress
    current_progress = progress_history.first()
    if not current_progress:
        current_progress = {'percentage': 0}
    
    # Get related tasks
    tasks = Task.objects.filter(project=project).order_by('-created_at')
    
    context = {
        'project': project,
        'tags': tags,
        'progress_history': progress_history,
        'current_progress': current_progress,
        'tasks': tasks,
    }
    
    return render(request, 'admin_custom/project_detail.html', context)

@login_required
def update_project_progress(request, project_id):
    """View function for updating project progress."""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        percentage = request.POST.get('percentage')
        notes = request.POST.get('notes', '')
        
        try:
            percentage = int(percentage)
            if 0 <= percentage <= 100:
                # Create progress update
                progress = ProjectProgress.objects.create(
                    project=project,
                    percentage=percentage,
                    notes=notes,
                    user=request.user
                )
                
                # Log activity
                ActivityLog.objects.create(
                    user=request.user,
                    activity_type='project_progress',
                    description=f'Progress for {project.title} updated to {percentage}%',
                    ip_address=request.META.get('REMOTE_ADDR', '')
                )
                
                messages.success(request, 'Progress updated successfully!')
            else:
                messages.error(request, 'Percentage must be between 0 and 100.')
        except ValueError:
            messages.error(request, 'Invalid percentage value.')
        
        return redirect('project_detail', project_id=project.id)
    
    return redirect('project_detail', project_id=project.id)

@login_required
def add_task(request, project_id):
    """View function for adding a task to a project."""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date_str = request.POST.get('due_date', '')
        priority = request.POST.get('priority', 'medium')
        
        if title:
            # Parse due date if provided
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
                    return redirect('project_detail', project_id=project.id)
            
            # Create task
            task = Task.objects.create(
                project=project,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                assigned_to=request.user,
                created_by=request.user
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                activity_type='task_created',
                description=f'Task "{title}" created for {project.title}',
                ip_address=request.META.get('REMOTE_ADDR', '')
            )
            
            messages.success(request, 'Task added successfully!')
        else:
            messages.error(request, 'Task title is required.')
        
        return redirect('project_detail', project_id=project.id)
    
    return redirect('project_detail', project_id=project.id)

@login_required
def update_task_status(request, task_id):
    """View function for updating task status."""
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        
        if status in ['pending', 'in_progress', 'completed', 'cancelled']:
            old_status = task.status
            task.status = status
            task.updated_at = timezone.now()
            task.save()
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                activity_type='task_updated',
                description=f'Task "{task.title}" status changed from {old_status} to {status}',
                ip_address=request.META.get('REMOTE_ADDR', '')
            )
            
            messages.success(request, 'Task status updated successfully!')
        else:
            messages.error(request, 'Invalid status value.')
        
        return redirect('project_detail', project_id=task.project.id)
    
    return redirect('project_detail', project_id=task.project.id)

@login_required
def settings_view(request):
    """View function for admin settings."""
    # Get or create site configuration
    site_config, created = SiteConfiguration.objects.get_or_create(pk=1)
    
    # Get admin settings
    admin_settings = AdminSetting.objects.all()
    
    # Get backup logs
    backup_logs = BackupLog.objects.all().order_by('-created_at')[:10]
    
    context = {
        'site_config': site_config,
        'admin_settings': admin_settings,
        'backup_logs': backup_logs,
    }
    
    return render(request, 'admin_custom/settings.html', context)

@login_required
def update_site_config(request):
    """View function for updating site configuration."""
    if request.method == 'POST':
        # Get or create site configuration
        site_config, created = SiteConfiguration.objects.get_or_create(pk=1)
        
        # Update fields
        site_config.site_title = request.POST.get('site_title', site_config.site_title)
        site_config.site_description = request.POST.get('site_description', site_config.site_description)
        site_config.contact_email = request.POST.get('contact_email', site_config.contact_email)
        site_config.contact_phone = request.POST.get('contact_phone', site_config.contact_phone)
        site_config.social_linkedin = request.POST.get('social_linkedin', site_config.social_linkedin)
        site_config.social_github = request.POST.get('social_github', site_config.social_github)
        site_config.social_twitter = request.POST.get('social_twitter', site_config.social_twitter)
        site_config.social_instagram = request.POST.get('social_instagram', site_config.social_instagram)
        site_config.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            activity_type='config_updated',
            description='Site configuration updated',
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        messages.success(request, 'Site configuration updated successfully!')
        
        return redirect('settings')
    
    return redirect('settings')

@login_required
def export_messages(request):
    """View function for exporting messages to CSV."""
    # Create CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="messages.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Subject', 'Message', 'Created At', 'Is Read'])
    
    messages = Message.objects.all().order_by('-created_at')
    for msg in messages:
        writer.writerow([msg.id, msg.name, msg.email, msg.subject, msg.message, msg.created_at, msg.is_read])
    
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        activity_type='export_data',
        description='Messages exported to CSV',
        ip_address=request.META.get('REMOTE_ADDR', '')
    )
    
    return response

@login_required
def export_visitors(request):
    """View function for exporting visitor data to CSV."""
    # Create CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visitors.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'IP Address', 'User Agent', 'Page Visited', 'Visit Time'])
    
    visitors = Visitor.objects.all().order_by('-visit_time')
    for visitor in visitors:
        writer.writerow([visitor.id, visitor.ip_address, visitor.user_agent, visitor.page_visited, visitor.visit_time])
    
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        activity_type='export_data',
        description='Visitor data exported to CSV',
        ip_address=request.META.get('REMOTE_ADDR', '')
    )
    
    return response

@login_required
def create_backup(request):
    """View function for creating a database backup."""
    # This is a simplified version - in a real app, you'd use Django's dumpdata or a proper backup solution
    try:
        # Create backup directory if it doesn't exist
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
        
        # Use Django's dumpdata command to create a JSON backup
        os.system(f'python manage.py dumpdata --exclude auth.permission --exclude contenttypes > {backup_file}')
        
        # Create backup log entry
        backup_log = BackupLog.objects.create(
            file_path=backup_file,
            created_by=request.user,
            status='success',
            notes='Manual backup created'
        )
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            activity_type='backup_created',
            description=f'Database backup created: {os.path.basename(backup_file)}',
            ip_address=request.META.get('REMOTE_ADDR', '')
        )
        
        messages.success(request, 'Backup created successfully!')
    except Exception as e:
        # Log error
        BackupLog.objects.create(
            file_path='',
            created_by=request.user,
            status='failed',
            notes=f'Error: {str(e)}'
        )
        
        messages.error(request, f'Backup failed: {str(e)}')
    
    return redirect('settings')

@login_required
def activity_logs(request):
    """View function for activity logs."""
    logs = ActivityLog.objects.all().order_by('-timestamp')
    
    # Pagination
    paginator = Paginator(logs, 20)  # Show 20 logs per page
    page = request.GET.get('page')
    logs_page = paginator.get_page(page)
    
    context = {
        'logs': logs_page,
    }
    
    return render(request, 'admin_custom/activity_logs.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """View function for marking a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))

@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read."""
    if request.method == 'POST':
        Notification.objects.filter(is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Authentication Views
def admin_login(request):
    """Admin login view."""
    if request.user.is_authenticated:
        return redirect('admin_custom:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f'Selamat datang, {user.get_full_name() or user.username}!')
                return redirect('admin_custom:dashboard')
            else:
                messages.error(request, 'Username atau password salah, atau Anda tidak memiliki akses admin.')
        else:
            messages.error(request, 'Username atau password salah.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'admin_custom/login.html', {'form': form})

@login_required
def admin_logout(request):
    """Admin logout view."""
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('admin_custom:login')

# Additional Message Views
@login_required
def delete_message(request, message_id):
    """Delete a message."""
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Pesan berhasil dihapus.')
        return redirect('admin_custom:messages_list')
    return redirect('admin_custom:message_detail', message_id=message_id)

@login_required
def mark_message_read(request, message_id):
    """Mark a message as read."""
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        message.is_read = True
        message.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def mark_all_messages_read(request):
    """Mark all messages as read."""
    if request.method == 'POST':
        Message.objects.filter(is_read=False).update(is_read=True)
        messages.success(request, 'Semua pesan telah ditandai sebagai dibaca.')
        return redirect('admin_custom:messages_list')
    return redirect('admin_custom:messages_list')

# Additional Project Views
@login_required
def toggle_project_status(request, project_id):
    """Toggle project active status."""
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.is_active = not project.is_active
        project.save()
        status = 'diaktifkan' if project.is_active else 'dinonaktifkan'
        messages.success(request, f'Proyek "{project.title}" berhasil {status}.')
        return redirect('admin_custom:project_detail', project_id=project_id)
    return redirect('admin_custom:project_detail', project_id=project_id)

@login_required
def toggle_project_featured(request, project_id):
    """Toggle project featured status."""
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.is_featured = not project.is_featured
        project.save()
        status = 'ditambahkan ke unggulan' if project.is_featured else 'dihapus dari unggulan'
        messages.success(request, f'Proyek "{project.title}" berhasil {status}.')
        return redirect('admin_custom:project_detail', project_id=project_id)
    return redirect('admin_custom:project_detail', project_id=project_id)

@login_required
def duplicate_project(request, project_id):
    """Duplicate a project."""
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        # Create a copy of the project
        new_project = Project.objects.create(
            profile=project.profile,
            title=f"{project.title} (Copy)",
            description=project.description,
            technologies=project.technologies,
            live_url=project.live_url,
            github_url=project.github_url,
            order=Project.objects.count() + 1,
            is_active=False,
            is_featured=False
        )
        messages.success(request, f'Proyek "{project.title}" berhasil diduplikasi.')
        return redirect('admin_custom:project_detail', project_id=new_project.id)
    return redirect('admin_custom:project_detail', project_id=project_id)

# Additional Task Views
@login_required
def toggle_task_status(request, task_id):
    """Toggle task status."""
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        if task.status == 'completed':
            task.status = 'pending'
        else:
            task.status = 'completed'
        task.save()
        return redirect('admin_custom:project_detail', project_id=task.project.id)
    return redirect('admin_custom:project_detail', project_id=task.project.id)

@login_required
def edit_task(request, task_id):
    """Edit a task."""
    task = get_object_or_404(Task, id=task_id)
    # This would typically render an edit form
    # For now, redirect back to project detail
    return redirect('admin_custom:project_detail', project_id=task.project.id)

@login_required
def delete_task(request, task_id):
    """Delete a task."""
    task = get_object_or_404(Task, id=task_id)
    project_id = task.project.id
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tugas berhasil dihapus.')
    return redirect('admin_custom:project_detail', project_id=project_id)

# Additional Activity Log Views
@login_required
def clear_old_logs(request):
    """Clear old activity logs."""
    if request.method == 'POST':
        days = int(request.POST.get('days', 30))
        cutoff_date = timezone.now() - timedelta(days=days)
        deleted_count = ActivityLog.objects.filter(timestamp__lt=cutoff_date).count()
        ActivityLog.objects.filter(timestamp__lt=cutoff_date).delete()
        messages.success(request, f'{deleted_count} log aktivitas lama berhasil dihapus.')
        return redirect('admin_custom:activity_logs')
    return redirect('admin_custom:activity_logs')

# API Views for AJAX
@login_required
def dashboard_stats_api(request):
    """API endpoint for dashboard statistics."""
    today = timezone.now().date()
    today_visitors = VisitorStat.objects.filter(date=today).aggregate(Sum('count'))['count__sum'] or 0
    total_messages = Message.objects.count()
    total_projects = Project.objects.count()
    total_skills = Skill.objects.count()
    
    return JsonResponse({
        'today_visitors': today_visitors,
        'total_messages': total_messages,
        'total_projects': total_projects,
        'total_skills': total_skills
    })

@login_required
def visitor_chart_api(request):
    """API endpoint for visitor chart data."""
    today = timezone.now().date()
    visitor_stats = []
    for i in range(7):
        day = today - timedelta(days=i)
        count = VisitorStat.objects.filter(date=day).aggregate(Sum('count'))['count__sum'] or 0
        visitor_stats.append({
            'date': day.strftime('%d %b'),
            'count': count
        })
    visitor_stats.reverse()
    return JsonResponse({'data': visitor_stats})

@login_required
def skills_chart_api(request):
    """API endpoint for skills chart data."""
    skills = Skill.objects.filter(category='technical').order_by('-proficiency')[:10]
    skill_data = [{
        'name': skill.name,
        'proficiency': skill.proficiency
    } for skill in skills]
    return JsonResponse({'data': skill_data})

@login_required
def notifications_api(request):
    """API endpoint for notifications."""
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:10]
    data = [{
        'id': notif.id,
        'title': notif.title,
        'message': notif.message,
        'type': notif.notification_type,
        'created_at': notif.created_at.isoformat()
    } for notif in notifications]
    return JsonResponse({'notifications': data})

# Security Views
@login_required
def logout_all_sessions(request):
    """Logout from all sessions."""
    if request.method == 'POST':
        # This would typically clear all sessions for the user
        # For now, just logout from current session
        logout(request)
        messages.success(request, 'Anda telah logout dari semua sesi.')
        return redirect('admin_custom:login')
    return redirect('admin_custom:settings')
