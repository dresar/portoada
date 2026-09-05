from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Profile(models.Model):
    """Model untuk profil utama"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    title = models.CharField(max_length=200, verbose_name="Jabatan/Title")
    bio = models.TextField(verbose_name="Biografi")
    short_bio = models.CharField(max_length=300, verbose_name="Bio Singkat")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Nomor Telepon")
    address = models.TextField(verbose_name="Alamat", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Kota", blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name="Negara", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Tanggal Lahir", blank=True, null=True)
    age = models.IntegerField(verbose_name="Usia", blank=True, null=True)
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    github = models.URLField(blank=True, null=True, verbose_name="GitHub")
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn")
    twitter = models.URLField(blank=True, null=True, verbose_name="Twitter")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram")
    profile_image = models.ImageField(upload_to='profile/', verbose_name="Foto Profil", blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', verbose_name="Foto Cover", blank=True, null=True)
    resume = models.FileField(upload_to='resume/', verbose_name="File CV", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def __str__(self):
        return self.name

class About(models.Model):
    """Model untuk halaman about"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='about')
    story_title = models.CharField(max_length=200, verbose_name="Judul Cerita")
    story_content = models.TextField(verbose_name="Cerita Saya")
    mission = models.TextField(verbose_name="Misi")
    vision = models.TextField(verbose_name="Visi")
    values = models.TextField(verbose_name="Nilai-nilai")
    hobbies = models.TextField(verbose_name="Hobi")
    languages = models.TextField(verbose_name="Bahasa yang Dikuasai")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tentang Saya"
        verbose_name_plural = "Tentang Saya"

    def __str__(self):
        return f"About - {self.profile.name}"

class Education(models.Model):
    """Model untuk pendidikan"""
    DEGREE_CHOICES = [
        ('SD', 'Sekolah Dasar'),
        ('SMP', 'Sekolah Menengah Pertama'),
        ('SMA', 'Sekolah Menengah Atas'),
        ('D3', 'Diploma 3'),
        ('D4', 'Diploma 4'),
        ('S1', 'Sarjana'),
        ('S2', 'Magister'),
        ('S3', 'Doktor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=200, verbose_name="Nama Institusi")
    degree = models.CharField(max_length=3, choices=DEGREE_CHOICES, verbose_name="Gelar")
    field_of_study = models.CharField(max_length=200, verbose_name="Bidang Studi")
    start_date = models.DateField(verbose_name="Tanggal Mulai")
    end_date = models.DateField(blank=True, null=True, verbose_name="Tanggal Selesai")
    is_current = models.BooleanField(default=False, verbose_name="Masih Berlangsung")
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, verbose_name="IPK")
    description = models.TextField(verbose_name="Deskripsi")
    achievements = models.TextField(blank=True, null=True, verbose_name="Pencapaian")
    logo = models.ImageField(upload_to='education/', blank=True, null=True, verbose_name="Logo Institusi")
    certificate = models.FileField(upload_to='education_certificates/', blank=True, null=True, verbose_name="Sertifikat")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pendidikan"
        verbose_name_plural = "Pendidikan"
        ordering = ['-end_date', '-start_date']

    def __str__(self):
        return f"{self.degree} - {self.institution}"

class Skill(models.Model):
    """Model untuk keahlian"""
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('database', 'Databases'),
        ('tools', 'Tools & Platforms'),
        ('design', 'Design & UI/UX'),
        ('other', 'Other Skills'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100, verbose_name="Nama Keahlian")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategori")
    percentage = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Persentase Kemahiran"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon")
    color = models.CharField(max_length=7, default="#3B82F6", verbose_name="Warna")
    years_experience = models.IntegerField(default=0, verbose_name="Tahun Pengalaman")
    is_featured = models.BooleanField(default=False, verbose_name="Keahlian Unggulan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Keahlian"
        verbose_name_plural = "Keahlian"
        ordering = ['-percentage', 'name']

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

class Project(models.Model):
    """Model untuk proyek"""
    STATUS_CHOICES = [
        ('completed', 'Selesai'),
        ('ongoing', 'Sedang Berlangsung'),
        ('planned', 'Direncanakan'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200, verbose_name="Judul Proyek")
    description = models.TextField(verbose_name="Deskripsi")
    short_description = models.CharField(max_length=300, verbose_name="Deskripsi Singkat")
    technologies = models.TextField(verbose_name="Teknologi yang Digunakan")
    features = models.TextField(blank=True, null=True, verbose_name="Fitur Utama")
    challenges = models.TextField(blank=True, null=True, verbose_name="Tantangan")
    solutions = models.TextField(blank=True, null=True, verbose_name="Solusi")
    github_url = models.URLField(blank=True, null=True, verbose_name="URL GitHub")
    live_url = models.URLField(blank=True, null=True, verbose_name="URL Live Demo")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL Video Demo")
    image = models.ImageField(upload_to='projects/', verbose_name="Gambar Proyek")
    start_date = models.DateField(verbose_name="Tanggal Mulai")
    end_date = models.DateField(blank=True, null=True, verbose_name="Tanggal Selesai")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed', verbose_name="Status")
    is_featured = models.BooleanField(default=False, verbose_name="Proyek Unggulan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proyek"
        verbose_name_plural = "Proyek"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Experience(models.Model):
    """Model untuk pengalaman kerja"""
    EMPLOYMENT_CHOICES = [
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200, verbose_name="Nama Perusahaan")
    position = models.CharField(max_length=200, verbose_name="Jabatan")
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES, verbose_name="Tipe Pekerjaan")
    location = models.CharField(max_length=200, verbose_name="Lokasi")
    start_date = models.DateField(verbose_name="Tanggal Mulai")
    end_date = models.DateField(blank=True, null=True, verbose_name="Tanggal Selesai")
    is_current = models.BooleanField(default=False, verbose_name="Masih Bekerja")
    description = models.TextField(verbose_name="Deskripsi Pekerjaan")
    achievements = models.TextField(blank=True, null=True, verbose_name="Pencapaian")
    technologies_used = models.TextField(blank=True, null=True, verbose_name="Teknologi yang Digunakan")
    company_logo = models.ImageField(upload_to='companies/', blank=True, null=True, verbose_name="Logo Perusahaan")
    company_website = models.URLField(blank=True, null=True, verbose_name="Website Perusahaan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pengalaman Kerja"
        verbose_name_plural = "Pengalaman Kerja"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.position} at {self.company}"

class Certificate(models.Model):
    """Model untuk sertifikat"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=200, verbose_name="Judul Sertifikat")
    issuer = models.CharField(max_length=200, verbose_name="Penerbit")
    issue_date = models.DateField(verbose_name="Tanggal Diterbitkan")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Tanggal Kadaluarsa")
    credential_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ID Kredensial")
    credential_url = models.URLField(blank=True, null=True, verbose_name="URL Kredensial")
    description = models.TextField(verbose_name="Deskripsi")
    skills_covered = models.TextField(blank=True, null=True, verbose_name="Keahlian yang Dicakup")
    certificate_file = models.FileField(upload_to='certificates/', verbose_name="File Sertifikat")
    certificate_image = models.ImageField(upload_to='certificates/', verbose_name="Gambar Sertifikat")
    is_featured = models.BooleanField(default=False, verbose_name="Sertifikat Unggulan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikat"
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.title} - {self.issuer}"

class Contact(models.Model):
    """Model untuk pesan kontak"""
    STATUS_CHOICES = [
        ('new', 'Baru'),
        ('read', 'Sudah Dibaca'),
        ('replied', 'Sudah Dibalas'),
        ('archived', 'Diarsipkan'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nama")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nomor Telepon")
    subject = models.CharField(max_length=200, verbose_name="Subjek")
    message = models.TextField(verbose_name="Pesan")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP Address")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pesan Kontak"
        verbose_name_plural = "Pesan Kontak"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Service(models.Model):
    """Model untuk layanan yang ditawarkan"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200, verbose_name="Judul Layanan")
    description = models.TextField(verbose_name="Deskripsi")
    icon = models.CharField(max_length=50, verbose_name="Icon")
    color = models.CharField(max_length=7, default="#3B82F6", verbose_name="Warna")
    price_range = models.CharField(max_length=100, blank=True, null=True, verbose_name="Range Harga")
    delivery_time = models.CharField(max_length=100, blank=True, null=True, verbose_name="Waktu Pengerjaan")
    features = models.TextField(blank=True, null=True, verbose_name="Fitur Layanan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Layanan"
        verbose_name_plural = "Layanan"
        ordering = ['title']

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """Model untuk testimonial"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='testimonials')
    client_name = models.CharField(max_length=100, verbose_name="Nama Klien")
    client_position = models.CharField(max_length=100, verbose_name="Jabatan Klien")
    client_company = models.CharField(max_length=100, verbose_name="Perusahaan Klien")
    testimonial = models.TextField(verbose_name="Testimonial")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating"
    )
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name="Foto Klien")
    project_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nama Proyek")
    is_featured = models.BooleanField(default=False, verbose_name="Testimonial Unggulan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonial"
        ordering = ['-rating', '-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"

class Blog(models.Model):
    """Model untuk blog"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200, verbose_name="Judul Artikel")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    excerpt = models.TextField(verbose_name="Ringkasan")
    content = models.TextField(verbose_name="Konten")
    featured_image = models.ImageField(upload_to='blogs/', verbose_name="Gambar Utama")
    tags = models.TextField(blank=True, null=True, verbose_name="Tags")
    read_time = models.IntegerField(default=5, verbose_name="Waktu Baca (menit)")
    views = models.IntegerField(default=0, verbose_name="Jumlah Views")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Status")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Tanggal Publikasi")
    is_featured = models.BooleanField(default=False, verbose_name="Artikel Unggulan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blog"
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

class Award(models.Model):
    """Model untuk penghargaan"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=200, verbose_name="Judul Penghargaan")
    issuer = models.CharField(max_length=200, verbose_name="Pemberi Penghargaan")
    date_received = models.DateField(verbose_name="Tanggal Diterima")
    description = models.TextField(verbose_name="Deskripsi")
    category = models.CharField(max_length=100, verbose_name="Kategori")
    certificate_image = models.ImageField(upload_to='awards/', blank=True, null=True, verbose_name="Gambar Sertifikat")
    is_featured = models.BooleanField(default=False, verbose_name="Penghargaan Unggulan")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Penghargaan"
        verbose_name_plural = "Penghargaan"
        ordering = ['-date_received']

    def __str__(self):
        return f"{self.title} - {self.issuer}"

class SocialMedia(models.Model):
    """Model untuk social media"""
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('medium', 'Medium'),
        ('dev.to', 'Dev.to'),
        ('stackoverflow', 'Stack Overflow'),
        ('behance', 'Behance'),
        ('dribbble', 'Dribbble'),
        ('figma', 'Figma'),
        ('discord', 'Discord'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_media')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name="Platform")
    url = models.URLField(verbose_name="URL")
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Username")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media"
        ordering = ['platform']

    def __str__(self):
        return f"{self.get_platform_display()} - {self.username or self.url}"

class BlogCategory(models.Model):
    """Model untuk kategori blog"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nama Kategori")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kategori Blog"
        verbose_name_plural = "Kategori Blog"
        ordering = ['name']

    def __str__(self):
        return self.name

class BlogTag(models.Model):
    """Model untuk tag blog"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name="Nama Tag")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tag Blog"
        verbose_name_plural = "Tag Blog"
        ordering = ['name']

    def __str__(self):
        return self.name

class BlogComment(models.Model):
    """Model untuk komentar blog"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, verbose_name="Nama")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    content = models.TextField(verbose_name="Konten")
    is_approved = models.BooleanField(default=False, verbose_name="Disetujui")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Komentar Blog"
        verbose_name_plural = "Komentar Blog"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} on {self.blog.title}"

class PortfolioSettings(models.Model):
    """Model untuk pengaturan portofolio"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='settings')
    site_title = models.CharField(max_length=100, verbose_name="Judul Website")
    site_description = models.TextField(verbose_name="Deskripsi Website")
    theme_color = models.CharField(max_length=7, default="#3B82F6", verbose_name="Warna Tema")
    accent_color = models.CharField(max_length=7, default="#8B5CF6", verbose_name="Warna Aksen")
    enable_animations = models.BooleanField(default=True, verbose_name="Aktifkan Animasi")
    enable_blog = models.BooleanField(default=True, verbose_name="Aktifkan Blog")
    enable_testimonials = models.BooleanField(default=True, verbose_name="Aktifkan Testimonial")
    enable_services = models.BooleanField(default=True, verbose_name="Aktifkan Layanan")
    enable_awards = models.BooleanField(default=True, verbose_name="Aktifkan Penghargaan")
    google_analytics = models.CharField(max_length=50, blank=True, null=True, verbose_name="Google Analytics ID")
    meta_keywords = models.TextField(blank=True, null=True, verbose_name="Meta Keywords")
    meta_author = models.CharField(max_length=100, blank=True, null=True, verbose_name="Meta Author")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pengaturan Portofolio"
        verbose_name_plural = "Pengaturan Portofolio"

    def __str__(self):
        return f"Settings - {self.profile.name}"
