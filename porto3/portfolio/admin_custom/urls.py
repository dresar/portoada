from django.urls import path
from . import views

app_name = 'admin_custom'

urlpatterns = [
    # Authentication
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Dashboard
    path('', views.admin_dashboard, name='dashboard'),
    
    # Messages
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    path('messages/<int:message_id>/respond/', views.respond_to_message, name='respond_message'),
    path('messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('messages/<int:message_id>/mark-read/', views.mark_message_read, name='mark_message_read'),
    path('messages/mark-all-read/', views.mark_all_messages_read, name='mark_all_messages_read'),
    path('messages/export/', views.export_messages, name='export_messages'),
    
    # Projects
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/toggle-status/', views.toggle_project_status, name='toggle_project_status'),
    path('projects/<int:project_id>/toggle-featured/', views.toggle_project_featured, name='toggle_project_featured'),
    path('projects/<int:project_id>/update-progress/', views.update_project_progress, name='update_project_progress'),
    path('projects/<int:project_id>/duplicate/', views.duplicate_project, name='duplicate_project'),
    path('projects/<int:project_id>/add-task/', views.add_task, name='add_task'),
    
    # Tasks
    path('tasks/<int:task_id>/toggle-status/', views.toggle_task_status, name='toggle_task_status'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    
    # Settings
    path('settings/', views.settings_view, name='settings'),
    path('settings/site-config/', views.update_site_config, name='update_site_config'),
    
    # Activity Logs
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('activity-logs/clear-old/', views.clear_old_logs, name='clear_old_logs'),
    
    # Backup
    path('backup/create/', views.create_backup, name='create_backup'),
    
    # Notifications
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Export
    path('export/visitors/', views.export_visitors, name='export_visitors'),
    
    # API endpoints for AJAX
    path('api/dashboard-stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
    path('api/visitor-chart/', views.visitor_chart_api, name='visitor_chart_api'),
    path('api/skills-chart/', views.skills_chart_api, name='skills_chart_api'),
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    
    # Security
    path('logout-all-sessions/', views.logout_all_sessions, name='logout_all_sessions'),
]