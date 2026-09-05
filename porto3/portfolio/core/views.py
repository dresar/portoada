from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Profile, Skill, Education, Experience, Service, Project, ProjectTag, Certificate, CertificateSkill, Message
from admin_custom.models import Visitor, VisitorStat, SiteConfiguration, ActivityLog, Notification, ContactResponse
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

# Create your views here.
def index(request):
    """View function for home page of site."""
    # Record visitor
    if not request.session.get('visitor_recorded'):
        visitor_ip = request.META.get('REMOTE_ADDR', '')
        visitor = Visitor.objects.create(
            ip_address=visitor_ip,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            page_visited='index'
        )
        
        # Update visitor stats for today
        today = datetime.date.today()
        visitor_stat, created = VisitorStat.objects.get_or_create(
            date=today,
            defaults={'count': 1}
        )
        if not created:
            visitor_stat.count += 1
            visitor_stat.save()
            
        request.session['visitor_recorded'] = True
    
    # Handle contact form submission
    if request.method == 'POST' and 'contact_form' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_content = request.POST.get('message')
        
        if name and email and message_content:
            # Save message to database
            message = Message.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_content
            )
            
            # Create notification for admin
            admin_users = User.objects.filter(is_staff=True)
            for admin in admin_users:
                Notification.objects.create(
                    user=admin,
                    title='New Contact Message',
                    content=f'New message from {name} ({email})',
                    notification_type='message'
                )
            
            # Log activity
            ActivityLog.objects.create(
                activity_type='contact_message',
                description=f'New contact message received from {name}',
                ip_address=request.META.get('REMOTE_ADDR', '')
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    # Get profile information
    profile = Profile.objects.first()
    
    # Get skills grouped by category
    technical_skills = Skill.objects.filter(category='technical').order_by('-proficiency')
    professional_skills = Skill.objects.filter(category='professional').order_by('-proficiency')
    
    # Get education history
    education = Education.objects.all().order_by('-end_date')
    
    # Get experience history
    experiences = Experience.objects.all().order_by('-end_date')
    
    # Get services
    services = Service.objects.all()
    
    # Get projects with their tags
    projects = Project.objects.all().order_by('-created')
    
    # Get certificates with their skills
    certificates = Certificate.objects.all().order_by('-issue_date')
    
    # Get site configuration
    site_config = SiteConfiguration.objects.first()
    
    context = {
        'profile': profile,
        'technical_skills': technical_skills,
        'professional_skills': professional_skills,
        'education': education,
        'experiences': experiences,
        'services': services,
        'projects': projects,
        'certificates': certificates,
        'site_config': site_config,
    }
    
    return render(request, 'index.html', context)

@csrf_exempt
def send_message(request):
    """API endpoint for sending messages via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            subject = data.get('subject', '')
            message_content = data.get('message')
            
            if not all([name, email, message_content]):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
            
            # Save message to database
            message = Message.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_content
            )
            
            # Create notification for admin
            admin_users = User.objects.filter(is_staff=True)
            for admin in admin_users:
                Notification.objects.create(
                    user=admin,
                    title='New Contact Message',
                    content=f'New message from {name} ({email})',
                    notification_type='message'
                )
            
            # Log activity
            ActivityLog.objects.create(
                activity_type='contact_message',
                description=f'New contact message received from {name}',
                ip_address=request.META.get('REMOTE_ADDR', '')
            )
            
            return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
