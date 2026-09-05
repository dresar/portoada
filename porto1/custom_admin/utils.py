import os
import re
import uuid
from django.conf import settings

def handle_file_upload(file, upload_to='uploads/'):
    """
    Handle file upload and return the file path
    """
    if not file:
        return None
        
    # Create directory if it doesn't exist
    upload_dir = os.path.join(settings.MEDIA_ROOT, upload_to)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_to, file.name)
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    with open(full_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    return file_path

def delete_file_if_exists(file_path):
    """
    Delete file if it exists
    """
    if not file_path:
        return
        
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_path):
        os.remove(full_path)
        
def slugify(text):
    """
    Convert text to slug format
    """
    # Replace spaces with hyphens
    text = text.lower().strip()
    text = re.sub(r'\s+', '-', text)
    # Remove special characters
    text = re.sub(r'[^\w\-]', '', text)
    # Remove duplicate hyphens
    text = re.sub(r'-+', '-', text)
    return text