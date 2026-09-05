import os
import django
import sys
from datetime import date, datetime

# Setup Django environment
sys.path.append('c:\\codingan ku\\projectporto\\porto4')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portofolio.settings')
django.setup()

from frontend.models import (
    SiteSettings, SkillCategory, Skill, Education, Experience,
    ProjectCategory, Project, Technology, CertificateCategory, Certificate,
    Service, Statistic, BlogCategory, BlogTag, BlogPost, ContactMessage,
    UserProfile, Testimonial, Award
)
from django.contrib.auth.models import User

def clear_all_data():
    """Hapus semua data dari database"""
    print("Menghapus semua data...")
    
    # Hapus semua data
    ContactMessage.objects.all().delete()
    BlogPost.objects.all().delete()
    BlogTag.objects.all().delete()
    BlogCategory.objects.all().delete()
    Award.objects.all().delete()
    Testimonial.objects.all().delete()
    Statistic.objects.all().delete()
    Service.objects.all().delete()
    Certificate.objects.all().delete()
    CertificateCategory.objects.all().delete()
    Project.objects.all().delete()
    Technology.objects.all().delete()
    ProjectCategory.objects.all().delete()
    Experience.objects.all().delete()
    Education.objects.all().delete()
    Skill.objects.all().delete()
    SkillCategory.objects.all().delete()
    UserProfile.objects.all().delete()
    SiteSettings.objects.all().delete()
    
    print("Semua data berhasil dihapus!")

def create_dummy_data():
    """Buat dummy data untuk database"""
    print("Membuat dummy data...")
    
    # 1. Site Settings
    site_settings = SiteSettings.objects.create(
        site_title="Expedient609 Portfolio",
        site_description="Full Stack Developer & UI/UX Designer Portfolio",
        email="eka.syahputra@example.com",
        phone="+62 812-3456-7890",
        address="Jakarta, Indonesia",
        github="https://github.com/expedient609",
        linkedin="https://linkedin.com/in/eka-syahputra",
        twitter="https://twitter.com/expedient609",
        instagram="https://instagram.com/expedient609",
        facebook="https://facebook.com/eka.syahputra",
        youtube="https://youtube.com/@expedient609",
        meta_keywords="portfolio, web developer, full stack, react, django",
        meta_description="Portfolio website of Eka Syahputra - Full Stack Developer"
    )
    
    # 2. Skill Categories
    frontend_cat = SkillCategory.objects.create(
        name="Frontend Development",
        icon="fas fa-code",
        description="Teknologi untuk pengembangan antarmuka pengguna"
    )
    
    backend_cat = SkillCategory.objects.create(
        name="Backend Development",
        icon="fas fa-server",
        description="Teknologi untuk pengembangan server-side"
    )
    
    database_cat = SkillCategory.objects.create(
        name="Database",
        icon="fas fa-database",
        description="Sistem manajemen basis data"
    )
    
    tools_cat = SkillCategory.objects.create(
        name="Tools & Others",
        icon="fas fa-tools",
        description="Tools dan teknologi pendukung"
    )
    
    # 3. Skills
    skills_data = [
        # Frontend
        {"name": "HTML5", "category": frontend_cat, "proficiency": 95, "icon": "fab fa-html5"},
        {"name": "CSS3", "category": frontend_cat, "proficiency": 90, "icon": "fab fa-css3-alt"},
        {"name": "JavaScript", "category": frontend_cat, "proficiency": 88, "icon": "fab fa-js-square"},
        {"name": "React", "category": frontend_cat, "proficiency": 85, "icon": "fab fa-react"},
        {"name": "Vue.js", "category": frontend_cat, "proficiency": 80, "icon": "fab fa-vuejs"},
        {"name": "Tailwind CSS", "category": frontend_cat, "proficiency": 90, "icon": "fas fa-palette"},
        
        # Backend
        {"name": "Python", "category": backend_cat, "proficiency": 90, "icon": "fab fa-python"},
        {"name": "Django", "category": backend_cat, "proficiency": 85, "icon": "fas fa-server"},
        {"name": "Node.js", "category": backend_cat, "proficiency": 82, "icon": "fab fa-node-js"},
        {"name": "Express.js", "category": backend_cat, "proficiency": 80, "icon": "fas fa-code"},
        {"name": "Laravel", "category": backend_cat, "proficiency": 75, "icon": "fab fa-laravel"},
        
        # Database
        {"name": "PostgreSQL", "category": database_cat, "proficiency": 85, "icon": "fas fa-database"},
        {"name": "MySQL", "category": database_cat, "proficiency": 80, "icon": "fas fa-database"},
        {"name": "MongoDB", "category": database_cat, "proficiency": 75, "icon": "fas fa-leaf"},
        
        # Tools
        {"name": "Git", "category": tools_cat, "proficiency": 90, "icon": "fab fa-git-alt"},
        {"name": "Docker", "category": tools_cat, "proficiency": 75, "icon": "fab fa-docker"},
        {"name": "AWS", "category": tools_cat, "proficiency": 70, "icon": "fab fa-aws"},
        {"name": "Figma", "category": tools_cat, "proficiency": 85, "icon": "fab fa-figma"},
    ]
    
    for skill_data in skills_data:
        Skill.objects.create(**skill_data)
    
    # 4. Education
    Education.objects.create(
        institution="Universitas Indonesia",
        degree="Sarjana Komputer",
        field_of_study="Teknik Informatika",
        start_date=date(2019, 8, 1),
        end_date=date(2023, 7, 31),
        gpa="3.75",
        location="Jakarta, Indonesia",
        description="Fokus pada pengembangan perangkat lunak, algoritma, dan struktur data. Aktif dalam organisasi mahasiswa dan berbagai kompetisi programming.",
        is_current=False
    )
    
    Education.objects.create(
        institution="SMA Negeri 1 Jakarta",
        degree="SMA",
        field_of_study="IPA",
        start_date=date(2016, 7, 1),
        end_date=date(2019, 6, 30),
        gpa="89.5",
        location="Jakarta, Indonesia",
        description="Juara 1 Olimpiade Matematika tingkat provinsi. Aktif dalam ekstrakurikuler robotika dan programming.",
        is_current=False
    )
    
    # 5. Experience
    Experience.objects.create(
        company="Tech Solutions Inc.",
        position="Full Stack Developer",
        location="Jakarta, Indonesia",
        start_date=date(2023, 1, 1),
        end_date=None,
        description="Mengembangkan dan memelihara aplikasi web menggunakan MERN Stack. Merancang dan mengimplementasikan API RESTful. Berpartisipasi dalam siklus pengembangan perangkat lunak Agile.",
        is_current=True
    )
    
    Experience.objects.create(
        company="Digital Agency Co.",
        position="Junior Web Developer",
        location="Jakarta, Indonesia",
        start_date=date(2022, 6, 1),
        end_date=date(2022, 12, 31),
        description="Membantu tim dalam mengembangkan fitur baru untuk situs web klien. Memperbaiki bug dan melakukan pengujian. Belajar dari senior developer dan berkontribusi pada proyek kecil.",
        is_current=False
    )
    
    Experience.objects.create(
        company="Freelance",
        position="Web Designer",
        location="Remote",
        start_date=date(2021, 2, 1),
        end_date=date(2022, 5, 31),
        description="Merancang dan membangun website statis untuk berbagai klien. Mengimplementasikan desain responsif menggunakan HTML, CSS, dan JavaScript. Berkomunikasi langsung dengan klien untuk memenuhi kebutuhan proyek.",
        is_current=False
    )
    
    # 6. Technologies
    tech_data = [
        {"name": "React.js", "icon": "fab fa-react"},
        {"name": "Node.js", "icon": "fab fa-node-js"},
        {"name": "Express", "icon": "fas fa-server"},
        {"name": "MongoDB", "icon": "fas fa-leaf"},
        {"name": "Vue.js", "icon": "fab fa-vuejs"},
        {"name": "Laravel", "icon": "fab fa-laravel"},
        {"name": "MySQL", "icon": "fas fa-database"},
        {"name": "JavaScript", "icon": "fab fa-js-square"},
        {"name": "Chart.js", "icon": "fas fa-chart-bar"},
        {"name": "Django", "icon": "fas fa-server"},
        {"name": "PostgreSQL", "icon": "fas fa-database"},
        {"name": "React Native", "icon": "fab fa-react"},
        {"name": "Firebase", "icon": "fas fa-fire"},
        {"name": "HTML5", "icon": "fab fa-html5"},
        {"name": "CSS3", "icon": "fab fa-css3-alt"},
        {"name": "Three.js", "icon": "fas fa-cube"}
    ]
    
    technologies = {}
    for tech_data_item in tech_data:
        tech = Technology.objects.create(**tech_data_item)
        technologies[tech_data_item["name"]] = tech
    
    # 7. Project Categories
    web_cat = ProjectCategory.objects.create(
        name="Web Development",
        description="Proyek pengembangan aplikasi web"
    )
    
    mobile_cat = ProjectCategory.objects.create(
        name="Mobile Development",
        description="Proyek pengembangan aplikasi mobile"
    )
    
    design_cat = ProjectCategory.objects.create(
        name="UI/UX Design",
        description="Proyek desain antarmuka pengguna"
    )
    
    # 8. Projects
    # Create projects
    project1 = Project.objects.create(
        title="E-Commerce Platform",
        slug="ecommerce-platform",
        description="Platform e-commerce lengkap dengan fitur keranjang belanja, pembayaran online, dan dashboard admin. Dibangun menggunakan React.js untuk frontend dan Node.js dengan Express untuk backend.",
        short_description="Platform e-commerce modern dengan fitur lengkap",
        category=web_cat,
        repo_url="https://github.com/expedient609/ecommerce-platform",
        live_url="https://ecommerce-demo.expedient609.com",
        image="projects/ecommerce-platform.jpg",
        start_date=date(2023, 10, 1),
        end_date=date(2023, 11, 15),
        is_featured=True
    )
    project1.technologies.set([technologies["React.js"], technologies["Node.js"], technologies["Express"], technologies["MongoDB"]])
    
    project2 = Project.objects.create(
        title="Task Management App",
        slug="task-management-app",
        description="Aplikasi manajemen tugas dengan fitur drag & drop, kolaborasi tim, dan notifikasi real-time. Menggunakan Vue.js dan Laravel dengan WebSocket untuk real-time updates.",
        short_description="Aplikasi manajemen tugas dengan kolaborasi tim",
        category=web_cat,
        repo_url="https://github.com/expedient609/task-manager",
        live_url="https://taskmanager.expedient609.com",
        image="projects/task-manager.jpg",
        start_date=date(2023, 8, 1),
        end_date=date(2023, 9, 20),
        is_featured=True
    )
    project2.technologies.set([technologies["Vue.js"], technologies["Laravel"], technologies["MySQL"]])
    
    project3 = Project.objects.create(
        title="Weather Dashboard",
        slug="weather-dashboard",
        description="Dashboard cuaca interaktif dengan visualisasi data, prediksi 7 hari, dan peta interaktif. Mengintegrasikan multiple weather APIs untuk data yang akurat.",
        short_description="Dashboard cuaca interaktif dengan visualisasi data",
        category=web_cat,
        repo_url="https://github.com/expedient609/weather-dashboard",
        live_url="https://weather.expedient609.com",
        image="projects/weather-dashboard.jpg",
        start_date=date(2023, 6, 1),
        end_date=date(2023, 7, 10),
        is_featured=True
    )
    project3.technologies.set([technologies["JavaScript"], technologies["Chart.js"]])
    
    project4 = Project.objects.create(
        title="Blog Platform",
        slug="blog-platform",
        description="Platform blog dengan sistem CMS, editor rich text, sistem komentar, dan SEO optimization. Dibangun dengan Django dan PostgreSQL untuk performa optimal.",
        short_description="Platform blog dengan CMS dan SEO optimization",
        category=web_cat,
        repo_url="https://github.com/expedient609/blog-platform",
        live_url="https://blog.expedient609.com",
        image="projects/blog-platform.jpg",
        start_date=date(2023, 4, 1),
        end_date=date(2023, 5, 25),
        is_featured=True
    )
    project4.technologies.set([technologies["Django"], technologies["PostgreSQL"]])
    
    project5 = Project.objects.create(
        title="Mobile Fitness App",
        slug="mobile-fitness-app",
        description="Aplikasi fitness mobile dengan tracking workout, nutrition planner, dan social features. Dibangun menggunakan React Native untuk cross-platform compatibility.",
        short_description="Aplikasi fitness mobile dengan tracking workout",
        category=mobile_cat,
        repo_url="https://github.com/expedient609/fitness-app",
        live_url="",
        image="projects/fitness-app.jpg",
        start_date=date(2023, 2, 1),
        end_date=date(2023, 3, 18),
        is_featured=True
    )
    project5.technologies.set([technologies["React Native"], technologies["Firebase"]])
    
    project6 = Project.objects.create(
        title="Portfolio Website",
        slug="portfolio-website",
        description="Website portfolio personal dengan animasi interaktif, dark/light mode, dan responsive design. Menggunakan vanilla JavaScript dan Three.js untuk efek visual.",
        short_description="Website portfolio dengan animasi interaktif",
        category=web_cat,
        repo_url="https://github.com/expedient609/portfolio",
        live_url="https://expedient609.com",
        image="projects/portfolio.jpg",
        start_date=date(2023, 11, 1),
        end_date=date(2023, 12, 1),
        is_featured=True
    )
    project6.technologies.set([technologies["HTML5"], technologies["CSS3"], technologies["JavaScript"], technologies["Three.js"]])
    
    # 8. Certificate Categories
    web_cert_cat = CertificateCategory.objects.create(
        name="Web Development",
        description="Sertifikat pengembangan web"
    )
    
    programming_cert_cat = CertificateCategory.objects.create(
        name="Programming",
        description="Sertifikat programming dan algoritma"
    )
    
    design_cert_cat = CertificateCategory.objects.create(
        name="Design",
        description="Sertifikat desain dan UX"
    )
    
    # 9. Certificates
    certificates_data = [
        {
            "title": "Sertifikasi Full Stack Web Developer",
            "issuer": "Dicoding Indonesia",
            "category": web_cert_cat,
            "icon_class": "fas fa-award",
            "color": "yellow-500",
            "date_issued": date(2023, 12, 15),
            "credential_id": "FSWD-2023-001",
            "credential_url": "https://dicoding.com/certificates/FSWD-2023-001",
            "description": "Sertifikasi komprehensif dalam pengembangan web full stack menggunakan JavaScript, React, Node.js, dan database.",
            "is_featured": True
        },
        {
            "title": "The Complete 2023 Web Development Bootcamp",
            "issuer": "Udemy",
            "category": web_cert_cat,
            "icon_class": "fas fa-certificate",
            "color": "blue-500",
            "date_issued": date(2023, 11, 20),
            "credential_id": "UC-WDB-2023-002",
            "credential_url": "https://udemy.com/certificate/UC-WDB-2023-002",
            "description": "Bootcamp intensif web development covering HTML, CSS, JavaScript, React, Node.js, dan deployment.",
            "is_featured": True
        },
        {
            "title": "Google UX Design Professional Certificate",
            "issuer": "Coursera",
            "category": design_cert_cat,
            "icon_class": "fas fa-file-invoice",
            "color": "green-500",
            "date_issued": date(2023, 10, 10),
            "credential_id": "GUXD-2023-003",
            "credential_url": "https://coursera.org/verify/GUXD-2023-003",
            "description": "Program sertifikasi profesional Google untuk UX Design, covering user research, wireframing, prototyping.",
            "is_featured": True
        },
        {
            "title": "JavaScript Algorithms and Data Structures",
            "issuer": "freeCodeCamp",
            "category": programming_cert_cat,
            "icon_class": "fas fa-code",
            "color": "purple-500",
            "date_issued": date(2023, 9, 5),
            "credential_id": "FCC-JS-2023-004",
            "credential_url": "https://freecodecamp.org/certification/expedient609/javascript-algorithms-and-data-structures",
            "description": "Sertifikasi dalam algoritma JavaScript dan struktur data, termasuk ES6, regex, dan debugging.",
            "is_featured": True
        },
        {
            "title": "React - The Complete Guide",
            "issuer": "Udemy",
            "category": web_cert_cat,
            "icon_class": "fab fa-react",
            "color": "cyan-500",
            "date_issued": date(2023, 8, 15),
            "credential_id": "UC-REACT-2023-005",
            "credential_url": "https://udemy.com/certificate/UC-REACT-2023-005",
            "description": "Kursus komprehensif React.js covering hooks, context, Redux, testing, dan deployment.",
            "is_featured": True
        },
        {
            "title": "Python for Everybody Specialization",
            "issuer": "University of Michigan - Coursera",
            "category": programming_cert_cat,
            "icon_class": "fab fa-python",
            "color": "yellow-400",
            "date_issued": date(2023, 7, 20),
            "credential_id": "PY4E-2023-006",
            "credential_url": "https://coursera.org/verify/PY4E-2023-006",
            "description": "Spesialisasi Python covering programming fundamentals, data structures, web scraping, dan databases.",
            "is_featured": True
        }
    ]
    
    for cert_data in certificates_data:
        Certificate.objects.create(**cert_data)
    
    # 10. Services
    services_data = [
        {
            "title": "Web Development",
            "short_description": "Pengembangan website dan aplikasi web modern",
            "description": "Pengembangan website dan aplikasi web modern menggunakan teknologi terkini seperti React, Vue.js, dan Django dengan fokus pada performa dan user experience.",
            "icon": "fas fa-code",
            "is_featured": True
        },
        {
            "title": "Mobile App Development",
            "short_description": "Pengembangan aplikasi mobile cross-platform",
            "description": "Pengembangan aplikasi mobile cross-platform menggunakan React Native dan Flutter untuk iOS dan Android dengan performa native.",
            "icon": "fas fa-mobile-alt",
            "is_featured": True
        },
        {
            "title": "UI/UX Design",
            "short_description": "Desain antarmuka pengguna yang menarik",
            "description": "Desain antarmuka pengguna yang menarik dan user experience yang optimal untuk website dan aplikasi dengan pendekatan user-centered design.",
            "icon": "fas fa-palette",
            "is_featured": True
        },
        {
            "title": "API Development",
            "short_description": "Pengembangan RESTful API dan GraphQL",
            "description": "Pengembangan RESTful API dan GraphQL untuk integrasi sistem dan aplikasi dengan dokumentasi lengkap dan security best practices.",
            "icon": "fas fa-server",
            "is_featured": True
        }
    ]
    
    for service_data in services_data:
        Service.objects.create(**service_data)
    
    # 11. Statistics
    stats_data = [
        {
            "title": "Projects Completed",
            "value": 50,
            "icon": "fas fa-project-diagram",
            "description": "Proyek yang telah diselesaikan",
            "is_featured": True
        },
        {
            "title": "Happy Clients",
            "value": 30,
            "icon": "fas fa-users",
            "description": "Klien yang puas",
            "is_featured": True
        },
        {
            "title": "Years Experience",
            "value": 3,
            "icon": "fas fa-calendar-alt",
            "description": "Tahun pengalaman",
            "is_featured": True
        },
        {
            "title": "Technologies Mastered",
            "value": 15,
            "icon": "fas fa-code",
            "description": "Teknologi yang dikuasai",
            "is_featured": True
        }
    ]
    
    for stat_data in stats_data:
        Statistic.objects.create(**stat_data)
    
    # 12. Blog Categories
    tech_blog_cat = BlogCategory.objects.create(
        name="Technology",
        description="Artikel tentang teknologi dan programming"
    )
    
    tutorial_blog_cat = BlogCategory.objects.create(
        name="Tutorial",
        description="Tutorial dan panduan programming"
    )
    
    # 13. Blog Tags
    tags_data = ["JavaScript", "React", "Python", "Django", "Web Development", "Tutorial", "Tips", "Best Practices"]
    blog_tags = []
    for tag_name in tags_data:
        tag = BlogTag.objects.create(name=tag_name)
        blog_tags.append(tag)
    
    # 14. Create User for Blog Posts
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@expedient609.com',
            'first_name': 'Eka',
            'last_name': 'Syahputra',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    
    # Create UserProfile for admin user
    user_profile, created = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'bio': 'Full Stack Developer dengan pengalaman 5+ tahun dalam pengembangan web menggunakan Django, React, dan teknologi modern lainnya.',
            'phone': '+62 812-3456-7890',
            'address': 'Jakarta, Indonesia',
            'website': 'https://expedient609.com',
            'linkedin': 'https://linkedin.com/in/eka-syahputra',
            'github': 'https://github.com/expedient609',
            'instagram': 'https://instagram.com/expedient609',
            'twitter': 'https://twitter.com/expedient609'
        }
    )
    
    # 15. Blog Posts
    blog1 = BlogPost.objects.create(
        title="Membangun Website Portfolio dengan Django dan Tailwind CSS",
        slug="membangun-website-portfolio-django-tailwind",
        author=admin_user,
        content="Panduan lengkap cara membuat website portfolio profesional menggunakan Django dan Tailwind CSS dengan fitur-fitur modern seperti dark mode, animasi, dan responsive design.",
        excerpt="Panduan lengkap cara membuat website portfolio profesional menggunakan Django dan Tailwind CSS dengan fitur-fitur modern.",
        category=tutorial_blog_cat,
        featured_image="blog/django-tailwind-portfolio.jpg",
        status='published',
        is_featured=True,
        published_date=datetime(2023, 12, 1, 10, 0, 0)
    )
    blog1.tags.set([blog_tags[3], blog_tags[4], blog_tags[5]])  # Django, Web Development, Tutorial
    
    blog2 = BlogPost.objects.create(
        title="10 Tips Optimasi Performa React Application",
        slug="10-tips-optimasi-performa-react",
        author=admin_user,
        content="Tips dan trik untuk mengoptimalkan performa aplikasi React, termasuk lazy loading, memoization, dan code splitting untuk aplikasi yang lebih cepat.",
        excerpt="Tips dan trik untuk mengoptimalkan performa aplikasi React, termasuk lazy loading, memoization, dan code splitting.",
        category=tech_blog_cat,
        featured_image="blog/react-optimization-tips.jpg",
        status='published',
        is_featured=True,
        published_date=datetime(2023, 11, 15, 14, 30, 0)
    )
    blog2.tags.set([blog_tags[1], blog_tags[4], blog_tags[6]])  # React, Web Development, Tips
    
    blog3 = BlogPost.objects.create(
        title="Panduan Lengkap REST API dengan Django REST Framework",
        slug="panduan-rest-api-django-rest-framework",
        author=admin_user,
        content="Tutorial komprehensif untuk membangun REST API yang robust menggunakan Django REST Framework, termasuk authentication, serialization, dan testing.",
        excerpt="Tutorial komprehensif untuk membangun REST API yang robust menggunakan Django REST Framework.",
        category=tutorial_blog_cat,
        featured_image="blog/django-rest-api-guide.jpg",
        status='published',
        is_featured=True,
        published_date=datetime(2023, 10, 20, 9, 15, 0)
    )
    blog3.tags.set([blog_tags[2], blog_tags[3], blog_tags[5]])  # Python, Django, Tutorial
    
    print("Dummy data berhasil dibuat!")
    print(f"- Users: {User.objects.count()}")
    print(f"- Site Settings: {SiteSettings.objects.count()}")
    print(f"- Skill Categories: {SkillCategory.objects.count()}")
    print(f"- Skills: {Skill.objects.count()}")
    print(f"- Education: {Education.objects.count()}")
    print(f"- Experience: {Experience.objects.count()}")
    print(f"- Technologies: {Technology.objects.count()}")
    print(f"- Project Categories: {ProjectCategory.objects.count()}")
    print(f"- Projects: {Project.objects.count()}")
    print(f"- Certificate Categories: {CertificateCategory.objects.count()}")
    print(f"- Certificates: {Certificate.objects.count()}")
    print(f"- Services: {Service.objects.count()}")
    print(f"- Statistics: {Statistic.objects.count()}")
    print(f"- Blog Categories: {BlogCategory.objects.count()}")
    print(f"- Blog Tags: {BlogTag.objects.count()}")
    print(f"- Blog Posts: {BlogPost.objects.count()}")

if __name__ == "__main__":
    # Hapus semua data lama
    clear_all_data()
    
    # Buat dummy data baru
    create_dummy_data()
    
    print("\nSelesai! Database telah diisi dengan dummy data.")