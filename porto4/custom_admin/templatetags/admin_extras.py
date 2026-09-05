from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """Get an attribute of an object dynamically from a string name"""
    try:
        if hasattr(obj, str(attr)):
            return getattr(obj, str(attr))
        return obj[attr]
    except (TypeError, KeyError, AttributeError):
        return None

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    try:
        return dictionary.get(key)
    except AttributeError:
        return None

@register.filter
def replace_underscore(value):
    """Replace underscores with spaces"""
    return str(value).replace('_', ' ')

@register.filter
def model_name(obj):
    """Get the model name of an object"""
    return obj.__class__.__name__.lower()

@register.filter
def verbose_name(obj):
    """Get the verbose name of a model"""
    return obj._meta.verbose_name

@register.filter
def verbose_name_plural(obj):
    """Get the verbose name plural of a model"""
    return obj._meta.verbose_name_plural