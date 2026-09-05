from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator

# 1. Personal Information
class PersonalInfo(models.Model):
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    bio_short = models.CharField(max_length=500, help_text='Ringkasan singkat untuk halaman home')
    bio_full = models.TextField(help_text='Biografi lengkap untuk halaman about')
    profile_image = models.ImageField(upload_to='personal/profile/', blank=True, null=True)
    favicon = models.ImageField(upload_to='personal/favicon/', blank=True, null=True, help_text='Favicon untuk website')
    birth_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Nomor telepon harus dalam format: '+999999999'. Maksimal 15 digit.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    cv = models.FileField(upload_to='personal/cv/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Personal Information'

# 2. Social Media
class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('other', 'Other'),
    ]
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='social_media')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    username = models.CharField(max_length=100, blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text='Class CSS untuk ikon (contoh: fa-facebook)')
    
    def __str__(self):
        return f"{self.personal_info.name} - {self.platform}"
    
    class Meta:
        verbose_name_plural = 'Social Media'

# 3. Education
class Education(models.Model):
    DEGREE_CHOICES = [
        ('high_school', 'Sekolah Menengah'),
        ('associate', 'Diploma'),
        ('bachelor', 'Sarjana'),
        ('master', 'Magister'),
        ('doctorate', 'Doktor'),
        ('certification', 'Sertifikasi'),
        ('other', 'Lainnya'),
    ]
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(4)])
    location = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='education/logos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.institution} - {self.degree} in {self.field_of_study}"
    
    class Meta:
        ordering = ['-end_date', '-start_date']
        verbose_name_plural = 'Education'

# 4. Skill Category
class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text='Class CSS untuk ikon (contoh: fa-code)')
    order = models.PositiveIntegerField(default=0, help_text='Urutan tampilan kategori')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Skill Categories'

# 5. Skill
class Skill(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='skills')
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text='Skill level dari 1-5')
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text='Class CSS untuk ikon')
    logo = models.ImageField(upload_to='skills/logos/', blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0, help_text='Tahun pengalaman')
    is_featured = models.BooleanField(default=False, help_text='Tampilkan di halaman utama')
    order = models.PositiveIntegerField(default=0, help_text='Urutan tampilan skill')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['category', 'order']

# 6. Project Category
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text='Class CSS untuk ikon')
    order = models.PositiveIntegerField(default=0, help_text='Urutan tampilan kategori')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Project Categories'

# 7. Project
class Project(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='projects')
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text='URL-friendly name')
    description_short = models.CharField(max_length=500, help_text='Deskripsi singkat untuk halaman daftar')
    description_full = models.TextField(help_text='Deskripsi lengkap untuk halaman detail')
    client = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_ongoing = models.BooleanField(default=False)
    technologies = models.ManyToManyField(Skill, related_name='used_in_projects', blank=True)
    website_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/')
    featured_image = models.ImageField(upload_to='projects/featured/', blank=True, null=True)
    model_3d = models.FileField(upload_to='projects/models/', blank=True, null=True, help_text='Upload model 3D dalam format .gltf atau .glb')
    is_featured = models.BooleanField(default=False, help_text='Tampilkan di halaman utama')
    order = models.PositiveIntegerField(default=0, help_text='Urutan tampilan proyek')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-is_featured', 'order', '-end_date', '-start_date']

# 8. Project Image
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text='Urutan tampilan gambar')
    
    def __str__(self):
        return f"{self.project.name} - Image {self.order}"
    
    class Meta:
        ordering = ['order']

# 9. Experience
class Experience(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True, help_text='Daftar tanggung jawab, pisahkan dengan baris baru')
    achievements = models.TextField(blank=True, null=True, help_text='Daftar pencapaian, pisahkan dengan baris baru')
    company_website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='experience/logos/', blank=True, null=True)
    skills_used = models.ManyToManyField(Skill, related_name='used_in_experiences', blank=True)
    is_featured = models.BooleanField(default=False, help_text='Tampilkan di halaman utama')
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    class Meta:
        ordering = ['-is_current', '-end_date', '-start_date']
        verbose_name_plural = 'Experience'

# 10. Certificate
class Certificate(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='related_certificates', blank=True)
    certificate_image = models.ImageField(upload_to='certificates/images/', blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/files/', blank=True, null=True)
    organization_logo = models.ImageField(upload_to='certificates/logos/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text='Tampilkan di halaman utama')
    
    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"
    
    class Meta:
        ordering = ['-issue_date']

# 11. Service
class Service(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text='Class CSS untuk ikon')
    image = models.ImageField(upload_to='services/images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text='Tampilkan di halaman utama')
    order = models.PositiveIntegerField(default=0, help_text='Urutan tampilan layanan')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']

# 12. Testimonial
class Testimonial(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='testimonials')
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True, null=True)
    testimonial_text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text='Rating dari 1-5')
    profile_image = models.ImageField(upload_to='testimonials/profiles/', blank=True, null=True)
    company_logo = models.ImageField(upload_to='testimonials/logos/', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text='Tampilkan di halaman utama')
    order = models.PositiveIntegerField(default=0, help_text='Urutan tampilan testimonial')
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    
    class Meta:
        ordering = ['order', '-date']

# 13. Contact Message
class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Baru'),
        ('read', 'Dibaca'),
        ('replied', 'Dibalas'),
        ('archived', 'Diarsipkan'),
    ]
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='contact_messages')
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=200)
    message = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-date_sent']

# 14. Blog Category
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Blog Categories'

# 15. Blog Post
class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True, help_text='Ringkasan singkat artikel')
    featured_image = models.ImageField(upload_to='blog/featured/', blank=True, null=True)
    categories = models.ManyToManyField(BlogCategory, related_name='posts', blank=True)
    tags = models.CharField(max_length=500, blank=True, null=True, help_text='Pisahkan tag dengan koma')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False, help_text='Tampilkan di halaman utama')
    view_count = models.PositiveIntegerField(default=0)
    related_projects = models.ManyToManyField(Project, related_name='related_posts', blank=True)
    related_skills = models.ManyToManyField(Skill, related_name='related_posts', blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_published', '-date_created']
