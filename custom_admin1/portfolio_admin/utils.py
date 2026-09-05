from django.http import JsonResponse
from django.template.loader import render_to_string

def render_form_to_json_response(request, form, form_template, form_url, form_title):
    """
    Render a form to a JSON response for AJAX modal forms.
    """
    context = {
        'form': form,
        'form_url': form_url,
        'form_title': form_title,
    }
    html_form = render_to_string(form_template, context, request=request)
    return JsonResponse({'html_form': html_form})

def prepare_list_view_context(model_class, object_list, page_title, model_name, create_url, headers):
    """
    Prepare context for generic list views.
    """
    # Prepare display fields for each object
    for obj in object_list:
        obj.display_fields = []
        for field in model_class.list_display:
            if hasattr(obj, f'get_{field}_display'):
                value = getattr(obj, f'get_{field}_display')()
            elif hasattr(obj, field):
                value = getattr(obj, field)
                # Handle image fields
                if hasattr(value, 'url'):
                    value = f'<img src="{value.url}" alt="{field}" class="h-10 w-10 rounded-full">' 
                # Handle boolean fields
                elif isinstance(value, bool):
                    value = '<i class="fas fa-check text-green-500"></i>' if value else '<i class="fas fa-times text-red-500"></i>'
                # Handle date fields
                elif hasattr(value, 'strftime'):
                    value = value.strftime('%d %b %Y')
                # Handle foreign key fields
                elif hasattr(value, 'pk'):
                    value = str(value)
            else:
                value = '-'
            obj.display_fields.append(value)
        
        # Add URLs for actions
        obj.update_url = f'{model_name.lower()}_update/{obj.pk}/'
        obj.delete_url = f'{model_name.lower()}_delete/{obj.pk}/'
    
    # Prepare context
    context = {
        'object_list': object_list,
        'page_title': page_title,
        'model_name': model_name,
        'model_name_plural': model_name + 's',
        'create_url': create_url,
        'headers': headers,
    }
    
    return context

def prepare_detail_view_context(obj, model_name, fields, update_url, delete_url, list_url):
    """
    Prepare context for generic detail views.
    """
    # Prepare fields for display
    display_fields = []
    for field in fields:
        if hasattr(obj, f'get_{field}_display'):
            value = getattr(obj, f'get_{field}_display')()
        elif hasattr(obj, field):
            value = getattr(obj, field)
            # Handle image fields
            if hasattr(value, 'url'):
                value = f'<img src="{value.url}" alt="{field}" class="h-32 w-32 rounded">' 
            # Handle boolean fields
            elif isinstance(value, bool):
                value = '<i class="fas fa-check text-green-500"></i>' if value else '<i class="fas fa-times text-red-500"></i>'
            # Handle date fields
            elif hasattr(value, 'strftime'):
                value = value.strftime('%d %b %Y')
            # Handle foreign key fields
            elif hasattr(value, 'pk'):
                value = str(value)
        else:
            value = '-'
        
        # Get field label
        if hasattr(obj.__class__, '_meta'):
            try:
                label = obj.__class__._meta.get_field(field).verbose_name
            except:
                label = field.replace('_', ' ').title()
        else:
            label = field.replace('_', ' ').title()
        
        display_fields.append({
            'label': label,
            'value': value
        })
    
    # Prepare context
    context = {
        'object': obj,
        'model_name': model_name,
        'fields': display_fields,
        'update_url': update_url,
        'delete_url': delete_url,
        'list_url': list_url,
    }
    
    return context