from django import template
from django.utils.safestring import mark_safe
from ..models import (
    Profile, About, Education, Skill, Project, Experience, 
    Certificate, Contact, Service, Testimonial, Blog, Award, 
    BlogCategory, BlogTag, BlogComment, SocialMedia, PortfolioSettings
)

register = template.Library()

@register.simple_tag
def get_model_count(model_name):
    """
    Return the count of objects for a given model.
    """
    model_map = {
        'profile': Profile,
        'about': About,
        'education': Education,
        'skill': Skill,
        'project': Project,
        'experience': Experience,
        'certificate': Certificate,
        'contact': Contact,
        'service': Service,
        'testimonial': Testimonial,
        'blog': Blog,
        'award': Award,
        'blog_category': BlogCategory,
        'blog_tag': BlogTag,
        'blog_comment': BlogComment,
        'social_media': SocialMedia,
        'portfolio_settings': PortfolioSettings,
    }
    
    if model_name in model_map:
        return model_map[model_name].objects.count()
    return 0

@register.simple_tag
def get_unread_contact_count():
    """
    Return the count of unread contact messages.
    """
    return Contact.objects.filter(is_read=False).count()

@register.filter
def format_date(date):
    """
    Format a date object to a readable string.
    """
    if date:
        return date.strftime('%d %b %Y')
    return ''

@register.filter
def truncate_text(text, length=100):
    """
    Truncate text to a specified length and add ellipsis.
    """
    if text and len(text) > length:
        return text[:length] + '...'
    return text

@register.filter
def display_boolean(value):
    """
    Display a boolean value as a check or X icon.
    """
    if value:
        return mark_safe('<i class="fas fa-check text-green-500"></i>')
    return mark_safe('<i class="fas fa-times text-red-500"></i>')

@register.filter
def display_image(image, css_class='h-10 w-10 rounded-full'):
    """
    Display an image with specified CSS class.
    """
    if image and hasattr(image, 'url'):
        return mark_safe(f'<img src="{image.url}" class="{css_class}" alt="Image">')
    return mark_safe('<div class="bg-gray-200 flex items-center justify-center ' + css_class + '"><i class="fas fa-image text-gray-400"></i></div>')

@register.inclusion_tag('portfolio_admin/includes/pagination.html')
def show_pagination(page_obj):
    """
    Render pagination for a page object.
    """
    return {'page_obj': page_obj}