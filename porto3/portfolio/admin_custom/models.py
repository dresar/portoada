from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import Profile, Project, Certificate, Message

# Create your models here.
class Visitor(models.Model):
    ip_address = models.CharField(max_length=100)
    user_agent = models.TextField(blank=True, null=True)
    page_visited = models.CharField(max_length=200)
    visit_time = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    os = models.CharField(max_length=100, blank=True, null=True)
    device = models.CharField(max_length=100, blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    visit_duration = models.IntegerField(default=0, help_text='Duration in seconds')
    
    def __str__(self):
        return f"{self.ip_address} - {self.visit_time}"

class VisitorStat(models.Model):
    date = models.DateField(unique=True)
    count = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    page_views = models.IntegerField(default=0)
    bounce_rate = models.FloatField(default=0, help_text='Percentage of visitors who navigate away after viewing only one page')
    avg_visit_duration = models.IntegerField(default=0, help_text='Average duration in seconds')
    
    def __str__(self):
        return f"Stats for {self.date}"
        
    class Meta:
        ordering = ['-date']

class AdminSetting(models.Model):
    THEME_CHOICES = (
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('system', 'System Default'),
    )
    
    SIDEBAR_POSITION_CHOICES = (
        ('left', 'Left'),
        ('right', 'Right'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_settings')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='system')
    sidebar_collapsed = models.BooleanField(default=False)
    sidebar_position = models.CharField(max_length=10, choices=SIDEBAR_POSITION_CHOICES, default='left')
    dashboard_widgets = models.TextField(blank=True, null=True, help_text='JSON configuration of dashboard widgets')
    notification_preferences = models.TextField(blank=True, null=True, help_text='JSON configuration of notification preferences')
    items_per_page = models.IntegerField(default=25, validators=[MinValueValidator(5), MaxValueValidator(100)])
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Settings for {self.user.username}"
        
    class Meta:
        verbose_name = 'Admin Setting'
        verbose_name_plural = 'Admin Settings'

class Notification(models.Model):
    TYPE_CHOICES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )
    
    CATEGORY_CHOICES = (
        ('system', 'System'),
        ('message', 'Message'),
        ('project', 'Project'),
        ('task', 'Task'),
        ('backup', 'Backup'),
        ('security', 'Security'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='info')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    link_text = models.CharField(max_length=100, blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    is_email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    related_object_type = models.CharField(max_length=100, blank=True, null=True)
    related_object_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

class ProjectProgress(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='progress_updates')
    percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.percentage}% progress for {self.project.title} on {self.date}"
        
    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')
    completion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_at']

class BackupLog(models.Model):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('in_progress', 'In Progress'),
    )
    
    TYPE_CHOICES = (
        ('full', 'Full Backup'),
        ('partial', 'Partial Backup'),
        ('scheduled', 'Scheduled Backup'),
        ('manual', 'Manual Backup'),
    )
    
    filename = models.CharField(max_length=255)
    backup_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='full')
    file_size = models.BigIntegerField(default=0, help_text='Size in bytes')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    storage_location = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.filename} - {self.created_at}"
        
    class Meta:
        ordering = ['-created_at']

class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'View'),
        ('export', 'Export'),
        ('import', 'Import'),
        ('backup', 'Backup'),
        ('restore', 'Restore'),
        ('other', 'Other'),
    )
    
    SEVERITY_CHOICES = (
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    action = models.CharField(max_length=15, choices=ACTION_CHOICES)
    content_type = models.CharField(max_length=100, blank=True, null=True, help_text='Model or entity type')
    object_id = models.CharField(max_length=100, blank=True, null=True, help_text='ID of the affected object')
    object_repr = models.CharField(max_length=200, blank=True, null=True, help_text='String representation of the object')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='info')
    is_system = models.BooleanField(default=False, help_text='Whether this was a system-generated activity')
    
    def __str__(self):
        user_str = self.user.username if self.user else 'System'
        return f"{user_str} - {self.action} - {self.timestamp}"
        
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

class ContactResponse(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
    
    message = models.ForeignKey('core.Message', on_delete=models.CASCADE, related_name='responses')
    subject = models.CharField(max_length=200)
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_responses')
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_responses')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    cc = models.TextField(blank=True, null=True, help_text='Comma-separated email addresses')
    bcc = models.TextField(blank=True, null=True, help_text='Comma-separated email addresses')
    attachments = models.TextField(blank=True, null=True, help_text='Comma-separated file paths')
    
    def __str__(self):
        return f"Response to {self.message.name} - {self.subject}"
        
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Response'
        verbose_name_plural = 'Contact Responses'

class SiteConfiguration(models.Model):
    # General Settings
    site_title = models.CharField(max_length=200, default='My Portfolio')
    site_tagline = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', null=True, blank=True)
    logo = models.ImageField(upload_to='site/', null=True, blank=True)
    logo_dark = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Logo for dark mode')
    footer_text = models.TextField(blank=True, null=True)
    copyright_text = models.CharField(max_length=255, blank=True, null=True)
    
    # Contact Information
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_address = models.TextField(blank=True, null=True)
    
    # Social Media
    social_links = models.TextField(blank=True, null=True, help_text='JSON format of social media links')
    
    # Analytics and SEO
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)
    google_tag_manager_id = models.CharField(max_length=50, blank=True, null=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True, null=True)
    robots_txt = models.TextField(blank=True, null=True, help_text='Content for robots.txt file')
    sitemap_enabled = models.BooleanField(default=True)
    
    # Appearance
    primary_color = models.CharField(max_length=20, blank=True, null=True, default='#007bff')
    secondary_color = models.CharField(max_length=20, blank=True, null=True, default='#6c757d')
    enable_dark_mode = models.BooleanField(default=True)
    default_theme = models.CharField(max_length=10, default='light', choices=(('light', 'Light'), ('dark', 'Dark')))
    custom_css = models.TextField(blank=True, null=True)
    custom_js = models.TextField(blank=True, null=True)
    
    # System
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True, null=True)
    cache_timeout = models.IntegerField(default=3600, help_text='Cache timeout in seconds')
    enable_registration = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.site_title
        
    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'


class APIKey(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    )
    
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True)
    prefix = models.CharField(max_length=8, unique=True, help_text='First 8 characters of the key for reference')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    allowed_ips = models.TextField(blank=True, null=True, help_text='Comma-separated list of allowed IP addresses')
    allowed_endpoints = models.TextField(blank=True, null=True, help_text='Comma-separated list of allowed API endpoints')
    
    def __str__(self):
        return f"{self.name} ({self.prefix}...)"
    
    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
        ordering = ['-created_at']


class ThirdPartyIntegration(models.Model):
    TYPE_CHOICES = (
        ('analytics', 'Analytics'),
        ('payment', 'Payment Gateway'),
        ('email', 'Email Service'),
        ('storage', 'Cloud Storage'),
        ('social', 'Social Media'),
        ('messaging', 'Messaging'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('pending', 'Pending Configuration'),
    )
    
    name = models.CharField(max_length=100)
    integration_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    provider = models.CharField(max_length=100)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)
    auth_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    webhook_url = models.URLField(blank=True, null=True)
    webhook_secret = models.CharField(max_length=255, blank=True, null=True)
    config = models.TextField(blank=True, null=True, help_text='JSON configuration for the integration')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_message = models.TextField(blank=True, null=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_integrations')
    
    def __str__(self):
        return f"{self.name} ({self.provider})"
    
    class Meta:
        verbose_name = 'Third-Party Integration'
        verbose_name_plural = 'Third-Party Integrations'
        ordering = ['name']
        unique_together = ['provider', 'name']


class DataExport(models.Model):
    FORMAT_CHOICES = (
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('xlsx', 'Excel'),
        ('pdf', 'PDF'),
        ('xml', 'XML'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    DATA_TYPE_CHOICES = (
        ('visitors', 'Visitors'),
        ('messages', 'Messages'),
        ('projects', 'Projects'),
        ('tasks', 'Tasks'),
        ('activity_logs', 'Activity Logs'),
        ('all', 'All Data'),
        ('custom', 'Custom Query'),
    )
    
    name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='csv')
    query_params = models.TextField(blank=True, null=True, help_text='JSON format of query parameters')
    date_range_start = models.DateField(null=True, blank=True)
    date_range_end = models.DateField(null=True, blank=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.BigIntegerField(default=0, help_text='Size in bytes')
    row_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='data_exports')
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=50, blank=True, null=True, help_text='Cron expression for scheduled exports')
    last_scheduled_run = models.DateTimeField(null=True, blank=True)
    notification_email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.data_type} - {self.format})"
    
    class Meta:
        verbose_name = 'Data Export'
        verbose_name_plural = 'Data Exports'
        ordering = ['-created_at']


class Report(models.Model):
    TYPE_CHOICES = (
        ('visitor', 'Visitor Analytics'),
        ('message', 'Message Analytics'),
        ('project', 'Project Analytics'),
        ('task', 'Task Analytics'),
        ('system', 'System Analytics'),
        ('custom', 'Custom Report'),
    )
    
    PERIOD_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom Range'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='monthly')
    custom_start_date = models.DateField(null=True, blank=True)
    custom_end_date = models.DateField(null=True, blank=True)
    config = models.TextField(blank=True, null=True, help_text='JSON configuration for the report')
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=50, blank=True, null=True, help_text='Cron expression for scheduled reports')
    recipients = models.TextField(blank=True, null=True, help_text='Comma-separated list of email addresses')
    last_generated = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_reports')
    
    def __str__(self):
        return f"{self.name} ({self.report_type} - {self.period})"
    
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['name']
