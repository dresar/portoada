from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random
from faker import Faker

from core.models import (
    Profile, Skill, Education, Experience, Service, Project, ProjectTag,
    Certificate, CertificateSkill, Message, Testimonial, BlogCategory,
    BlogPost, BlogTag, BlogComment, Contact, SocialLink
)
from admin_custom.models import (
    Visitor, VisitorStat, AdminSetting, Notification, ProjectProgress,
    Task, BackupLog, ActivityLog, ContactResponse, SiteConfiguration,
    APIKey, ThirdPartyIntegration, DataExport, Report
)

class Command(BaseCommand):
    help = 'Create dummy data for all models'

    def __init__(self):
        super().__init__()
        self.fake = Faker('id_ID')  # Indonesian locale

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating dummy data...'))
        
        # Create superuser if not exists
        self.create_superuser()
        
        # Create core data
        self.create_profile()
        self.create_skills()
        self.create_education()
        self.create_experience()
        self.create_services()
        self.create_projects()
        self.create_certificates()
        self.create_messages()
        self.create_testimonials()
        self.create_blog_data()
        self.create_contact()
        self.create_social_links()
        
        # Create admin custom data
        self.create_visitors()
        self.create_visitor_stats()
        self.create_admin_settings()
        self.create_notifications()
        self.create_project_progress()
        self.create_tasks()
        self.create_backup_logs()
        self.create_activity_logs()
        self.create_contact_responses()
        self.create_site_configuration()
        self.create_api_keys()
        self.create_third_party_integrations()
        self.create_data_exports()
        self.create_reports()
        
        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))

    def create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@portfolio.com',
                password='admin123',
                first_name='Admin',
                last_name='Portfolio'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: admin/admin123'))

    def create_profile(self):
        if Profile.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        profile = Profile.objects.create(
            user=user,
            name='Eka Pratama',
            email='eka.pratama@portfolio.com',
            location='Jakarta, Indonesia',
            bio='Seorang pengembang web berpengalaman dengan keahlian dalam Django, React, dan teknologi modern lainnya. Passionate dalam menciptakan solusi digital yang inovatif dan user-friendly.',
            short_intro='Pengembang web yang berpengalaman dalam menciptakan solusi digital inovatif.',
            social_github='https://github.com/ekapratama',
            social_linkedin='https://linkedin.com/in/ekapratama',
            social_twitter='https://twitter.com/ekapratama',
            social_youtube='https://youtube.com/@ekapratama',
            social_website='https://ekapratama.dev'
        )
        self.stdout.write(self.style.SUCCESS('Profile created'))
        return profile

    def create_skills(self):
        if Skill.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        technical_skills = [
            ('Python', 95), ('Django', 90), ('JavaScript', 88), ('React', 85),
            ('HTML/CSS', 92), ('PostgreSQL', 80), ('Docker', 75), ('Git', 90),
            ('AWS', 70), ('Redis', 65), ('Node.js', 78), ('Vue.js', 72)
        ]
        
        professional_skills = [
            ('Problem Solving', 95), ('Team Leadership', 85), ('Communication', 90),
            ('Project Management', 80), ('Critical Thinking', 88), ('Creativity', 85)
        ]
        
        for name, proficiency in technical_skills:
            Skill.objects.create(
                profile=profile,
                name=name,
                category='technical',
                proficiency=proficiency,
                icon=f'fab fa-{name.lower().replace("/", "-").replace(".", "-")}',
                is_featured=proficiency >= 85
            )
            
        for name, proficiency in professional_skills:
            Skill.objects.create(
                profile=profile,
                name=name,
                category='professional',
                proficiency=proficiency,
                icon='fas fa-star',
                is_featured=proficiency >= 85
            )
            
        self.stdout.write(self.style.SUCCESS('Skills created'))

    def create_education(self):
        if Education.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        educations = [
            {
                'profile': profile,
                'institution': 'Universitas Indonesia',
                'degree': 'Sarjana Komputer',
                'field_of_study': 'Ilmu Komputer',
                'start_date': datetime(2018, 8, 1).date(),
                'end_date': datetime(2022, 7, 31).date(),
                'is_current': False,
                'description': 'Fokus pada pengembangan perangkat lunak, algoritma, dan struktur data. Aktif dalam organisasi mahasiswa dan berbagai kompetisi programming.'
            },
            {
                'profile': profile,
                'institution': 'SMA Negeri 1 Jakarta',
                'degree': 'SMA',
                'field_of_study': 'IPA',
                'start_date': datetime(2015, 7, 1).date(),
                'end_date': datetime(2018, 6, 30).date(),
                'is_current': False,
                'description': 'Jurusan IPA dengan fokus pada Matematika dan Fisika. Aktif dalam ekstrakurikuler robotika dan olimpiade sains.'
            }
        ]
        
        for edu_data in educations:
            Education.objects.create(**edu_data)
            
        self.stdout.write(self.style.SUCCESS('Education created'))

    def create_experience(self):
        if Experience.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        experiences = [
            {
                'profile': profile,
                'title': 'Senior Full Stack Developer',
                'company': 'Tech Innovate Indonesia',
                'start_date': datetime(2022, 8, 1).date(),
                'end_date': None,
                'is_current': True,
                'description': 'Memimpin tim pengembangan aplikasi web menggunakan Django dan React. Bertanggung jawab atas arsitektur sistem dan mentoring junior developer.',
                'location': 'Jakarta, Indonesia'
            },
            {
                'profile': profile,
                'title': 'Full Stack Developer',
                'company': 'Digital Solutions Corp',
                'start_date': datetime(2021, 1, 15).date(),
                'end_date': datetime(2022, 7, 31).date(),
                'is_current': False,
                'description': 'Mengembangkan dan memelihara aplikasi e-commerce dengan Django backend dan Vue.js frontend. Mengoptimalkan performa database dan implementasi CI/CD.',
                'location': 'Jakarta, Indonesia'
            },
            {
                'profile': profile,
                'title': 'Junior Web Developer',
                'company': 'StartUp Hub',
                'start_date': datetime(2020, 6, 1).date(),
                'end_date': datetime(2020, 12, 31).date(),
                'is_current': False,
                'description': 'Membangun website company profile dan landing pages menggunakan HTML, CSS, JavaScript, dan WordPress.',
                'location': 'Jakarta, Indonesia'
            }
        ]
        
        for exp_data in experiences:
            Experience.objects.create(**exp_data)
            
        self.stdout.write(self.style.SUCCESS('Experience created'))

    def create_services(self):
        if Service.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        services = [
            {
                'profile': profile,
                'title': 'Web Development',
                'description': 'Pengembangan website dan aplikasi web modern menggunakan teknologi terkini seperti Django, React, dan Vue.js.',
                'icon': 'fas fa-code'
            },
            {
                'profile': profile,
                'title': 'Mobile App Development',
                'description': 'Pembuatan aplikasi mobile cross-platform menggunakan React Native dan Flutter.',
                'icon': 'fas fa-mobile-alt'
            },
            {
                'profile': profile,
                'title': 'API Development',
                'description': 'Pengembangan REST API dan GraphQL untuk integrasi sistem dan aplikasi mobile.',
                'icon': 'fas fa-server'
            },
            {
                'profile': profile,
                'title': 'Database Design',
                'description': 'Perancangan dan optimasi database untuk performa aplikasi yang optimal.',
                'icon': 'fas fa-database'
            },
            {
                'profile': profile,
                'title': 'DevOps & Deployment',
                'description': 'Setup server, CI/CD pipeline, dan deployment aplikasi ke cloud platform.',
                'icon': 'fas fa-cloud'
            },
            {
                'profile': profile,
                'title': 'Technical Consulting',
                'description': 'Konsultasi teknis untuk arsitektur sistem dan pemilihan teknologi yang tepat.',
                'icon': 'fas fa-lightbulb'
            }
        ]
        
        for service_data in services:
            Service.objects.create(**service_data)
            
        self.stdout.write(self.style.SUCCESS('Services created'))

    def create_projects(self):
        if Project.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        projects = [
            {
                'profile': profile,
                'title': 'E-Commerce Platform',
                'slug': 'e-commerce-platform',
                'description': 'Sebuah platform e-commerce yang komprehensif yang dibangun menggunakan Django dan React. Platform ini mencakup fitur-fitur seperti manajemen produk, sistem pembayaran terintegrasi, tracking pesanan, dan dashboard admin yang powerful.',
                'short_description': 'Platform e-commerce lengkap dengan fitur pembayaran, inventory management, dan dashboard admin.',
                'category': 'web',
                'status': 'completed',
                'client': 'PT. Digital Commerce',
                'completion_date': datetime(2023, 6, 30).date(),
                'demo_link': 'https://demo-ecommerce.com',
                'source_link': 'https://github.com/ekapratama/ecommerce',
                'is_featured': True
            },
            {
                'profile': profile,
                'title': 'Learning Management System',
                'slug': 'learning-management-system',
                'description': 'LMS yang dirancang untuk institusi pendidikan dengan fitur lengkap seperti video streaming, quiz interaktif, assignment submission, dan progress tracking.',
                'short_description': 'Sistem manajemen pembelajaran online dengan fitur video streaming dan quiz interaktif.',
                'category': 'web',
                'status': 'completed',
                'client': 'Universitas Digital',
                'completion_date': datetime(2023, 2, 28).date(),
                'demo_link': 'https://demo-lms.com',
                'source_link': 'https://github.com/ekapratama/lms',
                'is_featured': True
            },
            {
                'profile': profile,
                'title': 'Task Management App',
                'slug': 'task-management-app',
                'description': 'Aplikasi task management yang memungkinkan tim untuk berkolaborasi secara efektif dengan fitur real-time notifications, file sharing, dan progress tracking.',
                'short_description': 'Aplikasi manajemen tugas dengan fitur kolaborasi tim dan real-time notifications.',
                'category': 'web',
                'status': 'in_progress',
                'client': 'Internal Project',
                'demo_link': 'https://demo-taskapp.com',
                'source_link': 'https://github.com/ekapratama/taskapp',
                'is_featured': True
            },
            {
                'profile': profile,
                'title': 'Restaurant POS System',
                'slug': 'restaurant-pos-system',
                'description': 'Sistem POS yang komprehensif untuk industri restoran dengan fitur manajemen menu, inventory tracking, sales reporting, dan integrasi dengan payment gateway.',
                'short_description': 'Sistem Point of Sale untuk restoran dengan fitur inventory dan reporting.',
                'category': 'web',
                'status': 'completed',
                'client': 'Resto Chain Indonesia',
                'completion_date': datetime(2022, 8, 31).date(),
                'demo_link': 'https://demo-pos.com',
                'source_link': 'https://github.com/ekapratama/pos',
                'is_featured': False
            }
        ]
        
        for project_data in projects:
            project = Project.objects.create(**project_data)
            
            # Create project tags
            ProjectTag.objects.create(project=project, name='Django')
            ProjectTag.objects.create(project=project, name='React')
            ProjectTag.objects.create(project=project, name='PostgreSQL')
                
        self.stdout.write(self.style.SUCCESS('Projects created'))

    def create_certificates(self):
        if Certificate.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        certificates = [
            {
                'profile': profile,
                'title': 'AWS Certified Solutions Architect',
                'slug': 'aws-certified-solutions-architect',
                'organization': 'Amazon Web Services',
                'category': 'certification',
                'issue_date': datetime(2023, 5, 15).date(),
                'expiry_date': datetime(2026, 5, 15).date(),
                'credential_id': 'AWS-SAA-2023-001',
                'credential_url': 'https://aws.amazon.com/verification',
                'description': 'Sertifikasi untuk merancang dan deploy sistem yang scalable di AWS cloud platform.',
                'is_featured': True
            },
            {
                'profile': profile,
                'title': 'Google Cloud Professional Developer',
                'slug': 'google-cloud-professional-developer',
                'organization': 'Google Cloud',
                'category': 'certification',
                'issue_date': datetime(2023, 3, 20).date(),
                'expiry_date': datetime(2025, 3, 20).date(),
                'credential_id': 'GCP-PD-2023-002',
                'credential_url': 'https://cloud.google.com/certification',
                'description': 'Sertifikasi untuk pengembangan aplikasi di Google Cloud Platform.',
                'is_featured': True
            },
            {
                'profile': profile,
                'title': 'Django Advanced Certification',
                'slug': 'django-advanced-certification',
                'organization': 'Django Software Foundation',
                'category': 'certification',
                'issue_date': datetime(2022, 11, 10).date(),
                'expiry_date': None,
                'credential_id': 'DJANGO-ADV-2022-003',
                'credential_url': 'https://djangoproject.com/certification',
                'description': 'Sertifikasi tingkat lanjut untuk pengembangan aplikasi web dengan Django framework.',
                'is_featured': True
            }
        ]
        
        for cert_data in certificates:
            cert = Certificate.objects.create(**cert_data)
            
            # Add skills to certificates
            if 'AWS' in cert_data['title']:
                CertificateSkill.objects.create(certificate=cert, name='AWS', proficiency=70)
            if 'Django' in cert_data['title']:
                CertificateSkill.objects.create(certificate=cert, name='Django', proficiency=90)
            if 'Google Cloud' in cert_data['title']:
                CertificateSkill.objects.create(certificate=cert, name='Google Cloud', proficiency=75)
                
        self.stdout.write(self.style.SUCCESS('Certificates created'))

    def create_messages(self):
        if Message.objects.exists():
            return
            
        for i in range(20):
            Message.objects.create(
                name=self.fake.name(),
                email=self.fake.email(),
                subject=self.fake.sentence(nb_words=6),
                message=self.fake.text(max_nb_chars=500),
                is_read=random.choice([True, False]),
                is_replied=random.choice([True, False]),
                ip_address=self.fake.ipv4(),
                user_agent=self.fake.user_agent()
            )
            
        self.stdout.write(self.style.SUCCESS('Messages created'))

    def create_testimonials(self):
        if Testimonial.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        testimonials = [
            {
                'profile': profile,
                'name': 'Budi Santoso',
                'position': 'CEO',
                'company': 'PT. Digital Inovasi',
                'content': 'Eka adalah developer yang sangat profesional dan berpengalaman. Hasil kerjanya selalu melampaui ekspektasi kami.',
                'rating': 5,
                'is_featured': True
            },
            {
                'profile': profile,
                'name': 'Sari Dewi',
                'position': 'Product Manager',
                'company': 'StartUp Tech',
                'content': 'Kerjasama dengan Eka sangat menyenangkan. Dia selalu memberikan solusi terbaik untuk setiap tantangan teknis.',
                'rating': 5,
                'is_featured': True
            },
            {
                'profile': profile,
                'name': 'Ahmad Rahman',
                'position': 'CTO',
                'company': 'Fintech Solutions',
                'content': 'Expertise Eka dalam Django dan React sangat membantu kami dalam mengembangkan platform fintech yang robust.',
                'rating': 5,
                'is_featured': True
            }
        ]
        
        for testimonial_data in testimonials:
            Testimonial.objects.create(**testimonial_data)
            
        self.stdout.write(self.style.SUCCESS('Testimonials created'))

    def create_blog_data(self):
        if BlogCategory.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        # Create categories
        categories = [
            {'name': 'Web Development', 'slug': 'web-development'},
            {'name': 'Django', 'slug': 'django'},
            {'name': 'React', 'slug': 'react'},
            {'name': 'Tutorial', 'slug': 'tutorial'},
            {'name': 'Tips & Tricks', 'slug': 'tips-tricks'}
        ]
        
        for cat_data in categories:
            BlogCategory.objects.create(**cat_data)
            
        # Create blog posts
        categories = list(BlogCategory.objects.all())
        
        for i in range(10):
            post = BlogPost.objects.create(
                profile=profile,
                title=self.fake.sentence(nb_words=8),
                slug=self.fake.slug(),
                content=self.fake.text(max_nb_chars=2000),
                excerpt=self.fake.text(max_nb_chars=200),
                category=random.choice(categories),
                status='published' if random.choice([True, False]) else 'draft',
                is_featured=random.choice([True, False]),
                published_at=self.fake.date_time_between(start_date='-60d', end_date='now', tzinfo=timezone.get_current_timezone())
            )
            
            # Add random tags
            tag_names = ['Python', 'JavaScript', 'CSS', 'HTML', 'API', 'Database']
            for tag_name in random.sample(tag_names, random.randint(1, 3)):
                BlogTag.objects.create(post=post, name=tag_name)
            
        self.stdout.write(self.style.SUCCESS('Blog data created'))

    def create_contact(self):
        if Contact.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        Contact.objects.create(
            profile=profile,
            address='Jl. Sudirman No. 123, Jakarta Pusat, DKI Jakarta 10220',
            phone='+62 812-3456-7890',
            email='contact@ekapratama.dev',
            website='https://ekapratama.dev',
            google_map_embed='<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3966.521260322283!2d106.8195613!3d-6.2087634!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69f5390917b759%3A0x6b45e67356080477!2sSudirman%20Central%20Business%20District!5e0!3m2!1sen!2sid!4v1635724000000!5m2!1sen!2sid" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>',
            available_for_freelance=True
        )
        
        self.stdout.write(self.style.SUCCESS('Contact created'))

    def create_social_links(self):
        if SocialLink.objects.exists():
            return
            
        profile = Profile.objects.first()
        if not profile:
            return
            
        social_links = [
            {'platform': 'github', 'url': 'https://github.com/ekapratama', 'icon': 'fab fa-github', 'is_active': True},
            {'platform': 'linkedin', 'url': 'https://linkedin.com/in/ekapratama', 'icon': 'fab fa-linkedin', 'is_active': True},
            {'platform': 'twitter', 'url': 'https://twitter.com/ekapratama', 'icon': 'fab fa-twitter', 'is_active': True},
            {'platform': 'instagram', 'url': 'https://instagram.com/ekapratama', 'icon': 'fab fa-instagram', 'is_active': True},
            {'platform': 'youtube', 'url': 'https://youtube.com/@ekapratama', 'icon': 'fab fa-youtube', 'is_active': True}
        ]
        
        for link_data in social_links:
            SocialLink.objects.create(profile=profile, **link_data)
            
        self.stdout.write(self.style.SUCCESS('Social links created'))

    def create_visitors(self):
        if Visitor.objects.exists():
            return
            
        for i in range(100):
            Visitor.objects.create(
                ip_address=self.fake.ipv4(),
                user_agent=self.fake.user_agent(),
                page_visited=random.choice(['/', '/about', '/projects', '/contact', '/blog']),
                visit_time=self.fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone()),
                referrer=random.choice([None, 'https://google.com', 'https://facebook.com', 'https://twitter.com']),
                country=random.choice(['Indonesia', 'Malaysia', 'Singapore', 'Thailand']),
                city=random.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Kuala Lumpur']),
                browser=random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
                os=random.choice(['Windows', 'macOS', 'Linux', 'Android', 'iOS']),
                device=random.choice(['Desktop', 'Mobile', 'Tablet']),
                session_id=self.fake.uuid4(),
                visit_duration=random.randint(30, 600)
            )
            
        self.stdout.write(self.style.SUCCESS('Visitors created'))

    def create_visitor_stats(self):
        if VisitorStat.objects.exists():
            return
            
        for i in range(30):
            date = timezone.now().date() - timedelta(days=i)
            VisitorStat.objects.create(
                date=date,
                count=random.randint(10, 100),
                unique_visitors=random.randint(5, 80),
                page_views=random.randint(20, 200),
                bounce_rate=random.uniform(20, 80),
                avg_visit_duration=random.randint(60, 300)
            )
            
        self.stdout.write(self.style.SUCCESS('Visitor stats created'))

    def create_admin_settings(self):
        user = User.objects.get(username='admin')
        if not AdminSetting.objects.filter(user=user).exists():
            AdminSetting.objects.create(
                user=user,
                theme='light',
                sidebar_collapsed=False,
                sidebar_position='left',
                dashboard_widgets='{}',
                notification_preferences='{}',
                items_per_page=25,
                language='id',
                timezone='Asia/Jakarta'
            )
            
        self.stdout.write(self.style.SUCCESS('Admin settings created'))

    def create_notifications(self):
        if Notification.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        
        for i in range(15):
            Notification.objects.create(
                user=user,
                title=self.fake.sentence(nb_words=5),
                message=self.fake.text(max_nb_chars=200),
                notification_type=random.choice(['info', 'success', 'warning', 'error']),
                category=random.choice(['system', 'message', 'project', 'task', 'backup', 'security']),
                is_read=random.choice([True, False]),
                created_at=self.fake.date_time_between(start_date='-7d', end_date='now', tzinfo=timezone.get_current_timezone()),
                expires_at=self.fake.date_time_between(start_date='now', end_date='+30d', tzinfo=timezone.get_current_timezone()),
                icon=random.choice(['fas fa-info', 'fas fa-check', 'fas fa-exclamation', 'fas fa-times'])
            )
            
        self.stdout.write(self.style.SUCCESS('Notifications created'))

    def create_project_progress(self):
        if ProjectProgress.objects.exists():
            return
            
        projects = Project.objects.all()
        user = User.objects.get(username='admin')
        
        for project in projects:
            for i in range(random.randint(3, 8)):
                ProjectProgress.objects.create(
                    project=project,
                    percentage=random.randint(0, 100),
                    notes=self.fake.text(max_nb_chars=200),
                    date=self.fake.date_between(start_date='-30d', end_date='today'),
                    user=user
                )
                
        self.stdout.write(self.style.SUCCESS('Project progress created'))

    def create_tasks(self):
        if Task.objects.exists():
            return
            
        projects = Project.objects.all()
        user = User.objects.get(username='admin')
        
        for project in projects:
            for i in range(random.randint(5, 15)):
                Task.objects.create(
                    project=project,
                    title=self.fake.sentence(nb_words=4),
                    description=self.fake.text(max_nb_chars=300),
                    priority=random.choice(['low', 'medium', 'high', 'urgent']),
                    status=random.choice(['pending', 'in_progress', 'completed', 'cancelled']),
                    due_date=self.fake.date_between(start_date='today', end_date='+30d'),
                    assigned_to=user,
                    created_by=user,
                    completion_date=self.fake.date_between(start_date='-30d', end_date='today') if random.choice([True, False]) else None
                )
                
        self.stdout.write(self.style.SUCCESS('Tasks created'))

    def create_backup_logs(self):
        if BackupLog.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        
        for i in range(10):
            BackupLog.objects.create(
                filename=f'backup_{self.fake.date()}.sql',
                backup_type=random.choice(['full', 'partial', 'scheduled', 'manual']),
                file_size=random.randint(1000000, 100000000),
                created_at=self.fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone()),
                completed_at=self.fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone()),
                status=random.choice(['success', 'failed', 'in_progress']),
                notes=self.fake.text(max_nb_chars=200),
                created_by=user,
                storage_location='/backups/'
            )
            
        self.stdout.write(self.style.SUCCESS('Backup logs created'))

    def create_activity_logs(self):
        if ActivityLog.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        
        for i in range(50):
            ActivityLog.objects.create(
                user=user,
                action=random.choice(['create', 'update', 'delete', 'login', 'logout', 'view', 'export']),
                content_type=random.choice(['Project', 'Message', 'Task', 'User']),
                object_id=str(random.randint(1, 100)),
                object_repr=self.fake.sentence(nb_words=3),
                timestamp=self.fake.date_time_between(start_date='-30d', end_date='now', tzinfo=timezone.get_current_timezone()),
                ip_address=self.fake.ipv4(),
                user_agent=self.fake.user_agent(),
                details=self.fake.text(max_nb_chars=200),
                severity=random.choice(['info', 'warning', 'error', 'critical']),
                is_system=random.choice([True, False])
            )
            
        self.stdout.write(self.style.SUCCESS('Activity logs created'))

    def create_contact_responses(self):
        if ContactResponse.objects.exists():
            return
            
        messages = Message.objects.all()[:5]
        user = User.objects.get(username='admin')
        
        for message in messages:
            ContactResponse.objects.create(
                message=message,
                subject=f'Re: {message.subject}',
                response_text=self.fake.text(max_nb_chars=500),
                created_by=user,
                sent_by=user,
                status=random.choice(['draft', 'sent', 'failed']),
                sent_at=self.fake.date_time_between(start_date='-7d', end_date='now', tzinfo=timezone.get_current_timezone()) if random.choice([True, False]) else None
            )
            
        self.stdout.write(self.style.SUCCESS('Contact responses created'))

    def create_site_configuration(self):
        if SiteConfiguration.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        
        SiteConfiguration.objects.create(
            site_title='Eka Pratama Portfolio',
            site_tagline='Full Stack Developer & Tech Enthusiast',
            meta_description='Portfolio website of Eka Pratama, a full stack developer specializing in Django and React.',
            meta_keywords='portfolio, web developer, django, react, full stack',
            footer_text='Terima kasih telah mengunjungi portfolio saya.',
            copyright_text='© 2024 Eka Pratama. All rights reserved.',
            contact_email='contact@ekapratama.dev',
            contact_phone='+62 812-3456-7890',
            contact_address='Jakarta, Indonesia',
            google_analytics_id='GA-123456789',
            primary_color='#3B82F6',
            secondary_color='#6B7280',
            enable_dark_mode=True,
            default_theme='light',
            maintenance_mode=False,
            cache_timeout=3600,
            enable_registration=False,
            updated_by=user
        )
        
        self.stdout.write(self.style.SUCCESS('Site configuration created'))

    def create_api_keys(self):
        if APIKey.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        
        for i in range(3):
            key = self.fake.sha256()[:64]
            APIKey.objects.create(
                name=f'API Key {i+1}',
                key=key,
                prefix=key[:8],
                user=user,
                status=random.choice(['active', 'inactive']),
                expires_at=self.fake.date_time_between(start_date='+30d', end_date='+365d', tzinfo=timezone.get_current_timezone()),
                description=self.fake.text(max_nb_chars=100),
                allowed_ips='127.0.0.1,192.168.1.1',
                allowed_endpoints='/api/v1/projects,/api/v1/messages'
            )
            
        self.stdout.write(self.style.SUCCESS('API keys created'))

    def create_third_party_integrations(self):
        if ThirdPartyIntegration.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        
        integrations = [
            {
                'name': 'Google Analytics',
                'integration_type': 'analytics',
                'provider': 'Google',
                'status': 'active'
            },
            {
                'name': 'Stripe Payment',
                'integration_type': 'payment',
                'provider': 'Stripe',
                'status': 'active'
            },
            {
                'name': 'SendGrid Email',
                'integration_type': 'email',
                'provider': 'SendGrid',
                'status': 'inactive'
            }
        ]
        
        for integration_data in integrations:
            ThirdPartyIntegration.objects.create(
                created_by=user,
                **integration_data
            )
            
        self.stdout.write(self.style.SUCCESS('Third-party integrations created'))

    def create_data_exports(self):
        if DataExport.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        
        for i in range(5):
            DataExport.objects.create(
                name=f'Export {i+1}',
                data_type=random.choice(['visitors', 'messages', 'projects', 'tasks']),
                format=random.choice(['csv', 'json', 'xlsx']),
                date_range_start=self.fake.date_between(start_date='-30d', end_date='-15d'),
                date_range_end=self.fake.date_between(start_date='-15d', end_date='today'),
                file_path=f'/exports/export_{i+1}.csv',
                file_size=random.randint(1000, 50000),
                row_count=random.randint(10, 1000),
                status=random.choice(['pending', 'completed', 'failed']),
                created_by=user,
                notification_email='admin@portfolio.com'
            )
            
        self.stdout.write(self.style.SUCCESS('Data exports created'))

    def create_reports(self):
        if Report.objects.exists():
            return
            
        user = User.objects.get(username='admin')
        
        reports = [
            {
                'name': 'Monthly Visitor Report',
                'description': 'Laporan pengunjung bulanan',
                'report_type': 'visitor',
                'period': 'monthly'
            },
            {
                'name': 'Project Progress Report',
                'description': 'Laporan progress proyek',
                'report_type': 'project',
                'period': 'weekly'
            },
            {
                'name': 'Message Analytics',
                'description': 'Analisis pesan masuk',
                'report_type': 'message',
                'period': 'daily'
            }
        ]
        
        for report_data in reports:
            Report.objects.create(
                created_by=user,
                recipients='admin@portfolio.com',
                **report_data
            )
            
        self.stdout.write(self.style.SUCCESS('Reports created'))