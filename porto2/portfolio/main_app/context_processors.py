from .models import PersonalInfo, SocialMedia

def personal_info(request):
    """
    Context processor untuk menyediakan informasi personal dan media sosial ke semua template
    """
    # Ambil informasi personal dari database
    info = PersonalInfo.objects.first()
    
    # Ambil media sosial jika informasi personal tersedia
    social_media = []
    if info:
        social_media = SocialMedia.objects.filter(personal_info=info)
        
        # Untuk kemudahan penggunaan di template, gunakan bio sebagai alias untuk bio_short
        # dan bio_full tetap tersedia jika dibutuhkan
        info.bio = info.bio_short
    
    # Return dictionary yang akan tersedia di semua template
    return {
        'global_personal_info': info,
        'global_social_media': social_media
    }