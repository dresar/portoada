import os
import json
import django
import datetime
from django.core.files.base import ContentFile
from django.utils.text import slugify

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

# Import models
from main_app.models import (
    PersonalInfo, SocialMedia, Education, SkillCategory, Skill,
    ProjectCategory, Project, ProjectImage, Experience, Certificate,
    Service, Testimonial, BlogCategory, BlogPost
)

# Load dummy data
with open('dummy_data.json', 'r') as f:
    data = json.load(f)

# Helper function to create placeholder images
def create_placeholder_image(model_instance, field_name, filename):
    """Create a simple placeholder image for the given model instance and field"""
    from PIL import Image, ImageDraw, ImageFont
    import io
    
    # Create a colored background image
    img = Image.new('RGB', (800, 600), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    
    # Add some text
    text = f"{field_name} for {model_instance}"
    d.text((10, 10), text, fill=(255, 255, 255))
    
    # Save to a bytes buffer
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    
    # Get the field
    field = getattr(model_instance, field_name)
    field.save(filename, ContentFile(buffer.read()), save=False)
    model_instance.save()

# Import data
def import_data():
    print("Starting data import...")
    
    # Clear existing data (optional - be careful in production!)
    # Uncomment these lines if you want to clear existing data
    # PersonalInfo.objects.all().delete()
    # SocialMedia.objects.all().delete()
    # Education.objects.all().delete()
    # SkillCategory.objects.all().delete()
    # Skill.objects.all().delete()
    # ProjectCategory.objects.all().delete()
    # Project.objects.all().delete()
    # ProjectImage.objects.all().delete()
    # Experience.objects.all().delete()
    # Certificate.objects.all().delete()
    # Service.objects.all().delete()
    # Testimonial.objects.all().delete()
    # BlogCategory.objects.all().delete()
    # BlogPost.objects.all().delete()
    
    # 1. Create PersonalInfo
    personal_info_data = data['personal_info']
    personal_info, created = PersonalInfo.objects.get_or_create(
        name=personal_info_data['name'],
        defaults={
            'job_title': personal_info_data['job_title'],
            'bio_short': personal_info_data['bio_short'],
            'bio_full': personal_info_data['bio_full'],
            'birth_date': datetime.datetime.strptime(personal_info_data['birth_date'], '%Y-%m-%d').date() if personal_info_data.get('birth_date') else None,
            'address': personal_info_data.get('address'),
            'phone_number': personal_info_data.get('phone_number'),
            'email': personal_info_data.get('email'),
            'website': personal_info_data.get('website'),
        }
    )
    
    if created:
        print(f"Created PersonalInfo: {personal_info.name}")
        # Create placeholder images
        create_placeholder_image(personal_info, 'profile_image', 'profile.jpg')
        create_placeholder_image(personal_info, 'favicon', 'favicon.ico')
    else:
        print(f"Using existing PersonalInfo: {personal_info.name}")
    
    # 2. Create Social Media
    for social_media_data in data['social_media']:
        social_media, created = SocialMedia.objects.get_or_create(
            personal_info=personal_info,
            platform=social_media_data['platform'],
            defaults={
                'url': social_media_data['url'],
                'username': social_media_data.get('username'),
                'icon_class': social_media_data.get('icon_class'),
            }
        )
        if created:
            print(f"Created SocialMedia: {social_media.platform}")
    
    # 3. Create Education
    for education_data in data['education']:
        education, created = Education.objects.get_or_create(
            personal_info=personal_info,
            institution=education_data['institution'],
            degree=education_data['degree'],
            field_of_study=education_data['field_of_study'],
            defaults={
                'start_date': datetime.datetime.strptime(education_data['start_date'], '%Y-%m-%d').date(),
                'end_date': datetime.datetime.strptime(education_data['end_date'], '%Y-%m-%d').date() if education_data.get('end_date') else None,
                'is_current': education_data.get('is_current', False),
                'description': education_data.get('description'),
                'gpa': education_data.get('gpa'),
                'location': education_data.get('location'),
                'website': education_data.get('website'),
            }
        )
        if created:
            print(f"Created Education: {education.institution} - {education.degree}")
            # Create placeholder image
            create_placeholder_image(education, 'logo', f"{slugify(education.institution)}_logo.jpg")
    
    # 4. Create Skill Categories
    skill_categories = {}
    for category_data in data['skill_categories']:
        category, created = SkillCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'description': category_data.get('description'),
                'icon_class': category_data.get('icon_class'),
                'order': category_data.get('order', 0),
            }
        )
        skill_categories[category.name] = category
        if created:
            print(f"Created SkillCategory: {category.name}")
    
    # 5. Create Skills
    skills = {}
    for skill_data in data['skills']:
        category = skill_categories.get(skill_data['category'])
        if category:
            skill, created = Skill.objects.get_or_create(
                personal_info=personal_info,
                category=category,
                name=skill_data['name'],
                defaults={
                    'description': skill_data.get('description'),
                    'level': skill_data.get('level', 3),
                    'icon_class': skill_data.get('icon_class'),
                    'years_of_experience': skill_data.get('years_of_experience', 0),
                    'is_featured': skill_data.get('is_featured', False),
                    'order': skill_data.get('order', 0),
                }
            )
            skills[skill.name] = skill
            if created:
                print(f"Created Skill: {skill.name}")
                # Create placeholder image
                create_placeholder_image(skill, 'logo', f"{slugify(skill.name)}_logo.jpg")
    
    # 6. Create Project Categories
    project_categories = {}
    for category_data in data['project_categories']:
        category, created = ProjectCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'description': category_data.get('description'),
                'icon_class': category_data.get('icon_class'),
                'order': category_data.get('order', 0),
            }
        )
        project_categories[category.name] = category
        if created:
            print(f"Created ProjectCategory: {category.name}")
    
    # 7. Create Projects
    projects = {}
    for project_data in data['projects']:
        category = project_categories.get(project_data['category'])
        if category:
            project, created = Project.objects.get_or_create(
                personal_info=personal_info,
                name=project_data['name'],
                defaults={
                    'category': category,
                    'slug': project_data['slug'],
                    'description_short': project_data.get('description_short'),
                    'description_full': project_data.get('description_full'),
                    'client': project_data.get('client'),
                    'start_date': datetime.datetime.strptime(project_data['start_date'], '%Y-%m-%d').date(),
                    'end_date': datetime.datetime.strptime(project_data['end_date'], '%Y-%m-%d').date() if project_data.get('end_date') else None,
                    'is_ongoing': project_data.get('is_ongoing', False),
                    'website_url': project_data.get('website_url'),
                    'github_url': project_data.get('github_url'),
                    'is_featured': project_data.get('is_featured', False),
                    'order': project_data.get('order', 0),
                }
            )
            
            # Add technologies (skills)
            if created and 'technologies' in project_data:
                for tech_name in project_data['technologies']:
                    if tech_name in skills:
                        project.technologies.add(skills[tech_name])
            
            projects[project.name] = project
            if created:
                print(f"Created Project: {project.name}")
                # Create placeholder images
                create_placeholder_image(project, 'thumbnail', f"{slugify(project.name)}_thumbnail.jpg")
                create_placeholder_image(project, 'featured_image', f"{slugify(project.name)}_featured.jpg")
    
    # 8. Create Project Images
    for image_data in data['project_images']:
        project = projects.get(image_data['project'])
        if project:
            image, created = ProjectImage.objects.get_or_create(
                project=project,
                title=image_data.get('title', f"Image for {project.name}"),
                defaults={
                    'description': image_data.get('description'),
                    'order': image_data.get('order', 0),
                }
            )
            if created:
                print(f"Created ProjectImage: {image.title}")
                # Create placeholder image
                create_placeholder_image(image, 'image', f"{slugify(project.name)}_{slugify(image.title)}.jpg")
    
    # 9. Create Experiences
    for experience_data in data['experiences']:
        experience, created = Experience.objects.get_or_create(
            personal_info=personal_info,
            company=experience_data['company'],
            position=experience_data['position'],
            defaults={
                'location': experience_data.get('location'),
                'start_date': datetime.datetime.strptime(experience_data['start_date'], '%Y-%m-%d').date(),
                'end_date': datetime.datetime.strptime(experience_data['end_date'], '%Y-%m-%d').date() if experience_data.get('end_date') else None,
                'is_current': experience_data.get('is_current', False),
                'description': experience_data.get('description'),
                'responsibilities': experience_data.get('responsibilities'),
                'achievements': experience_data.get('achievements'),
                'company_website': experience_data.get('company_website'),
                'is_featured': experience_data.get('is_featured', False),
            }
        )
        
        # Add skills used
        if created and 'skills_used' in experience_data:
            for skill_name in experience_data['skills_used']:
                if skill_name in skills:
                    experience.skills_used.add(skills[skill_name])
        
        if created:
            print(f"Created Experience: {experience.position} at {experience.company}")
            # Create placeholder image
            create_placeholder_image(experience, 'company_logo', f"{slugify(experience.company)}_logo.jpg")
    
    # 10. Create Certificates
    for certificate_data in data['certificates']:
        certificate, created = Certificate.objects.get_or_create(
            personal_info=personal_info,
            name=certificate_data['name'],
            issuing_organization=certificate_data['issuing_organization'],
            defaults={
                'issue_date': datetime.datetime.strptime(certificate_data['issue_date'], '%Y-%m-%d').date(),
                'expiration_date': datetime.datetime.strptime(certificate_data['expiration_date'], '%Y-%m-%d').date() if certificate_data.get('expiration_date') else None,
                'credential_id': certificate_data.get('credential_id'),
                'credential_url': certificate_data.get('credential_url'),
                'description': certificate_data.get('description'),
                'is_featured': certificate_data.get('is_featured', False),
            }
        )
        
        # Add related skills
        if created and 'skills' in certificate_data:
            for skill_name in certificate_data['skills']:
                if skill_name in skills:
                    certificate.skills.add(skills[skill_name])
        
        if created:
            print(f"Created Certificate: {certificate.name}")
            # Create placeholder images
            create_placeholder_image(certificate, 'certificate_image', f"{slugify(certificate.name)}_cert.jpg")
            create_placeholder_image(certificate, 'organization_logo', f"{slugify(certificate.issuing_organization)}_logo.jpg")
    
    # 11. Create Services
    for service_data in data['services']:
        service, created = Service.objects.get_or_create(
            personal_info=personal_info,
            title=service_data['title'],
            defaults={
                'description': service_data.get('description'),
                'icon_class': service_data.get('icon_class'),
                'is_featured': service_data.get('is_featured', False),
                'order': service_data.get('order', 0),
            }
        )
        if created:
            print(f"Created Service: {service.title}")
            # Create placeholder image
            create_placeholder_image(service, 'image', f"{slugify(service.title)}_image.jpg")
    
    # 12. Create Testimonials
    for testimonial_data in data['testimonials']:
        testimonial, created = Testimonial.objects.get_or_create(
            personal_info=personal_info,
            name=testimonial_data['name'],
            position=testimonial_data['position'],
            defaults={
                'company': testimonial_data.get('company'),
                'testimonial_text': testimonial_data.get('testimonial_text'),
                'rating': testimonial_data.get('rating', 5),
                'date': datetime.datetime.strptime(testimonial_data['date'], '%Y-%m-%d').date() if testimonial_data.get('date') else None,
                'is_featured': testimonial_data.get('is_featured', False),
                'order': testimonial_data.get('order', 0),
            }
        )
        if created:
            print(f"Created Testimonial: {testimonial.name} from {testimonial.company}")
            # Create placeholder images
            create_placeholder_image(testimonial, 'profile_image', f"{slugify(testimonial.name)}_profile.jpg")
            if testimonial.company:
                create_placeholder_image(testimonial, 'company_logo', f"{slugify(testimonial.company)}_logo.jpg")
    
    # 13. Create Blog Categories
    blog_categories = {}
    for category_data in data['blog_categories']:
        category, created = BlogCategory.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'slug': category_data.get('slug', slugify(category_data['name'])),
                'description': category_data.get('description'),
            }
        )
        blog_categories[category.name] = category
        if created:
            print(f"Created BlogCategory: {category.name}")
    
    # 14. Create Blog Posts
    for post_data in data['blog_posts']:
        post, created = BlogPost.objects.get_or_create(
            personal_info=personal_info,
            title=post_data['title'],
            defaults={
                'slug': post_data.get('slug', slugify(post_data['title'])),
                'content': post_data.get('content'),
                'excerpt': post_data.get('excerpt'),
                'tags': post_data.get('tags'),
                'status': post_data.get('status', 'draft'),
                'date_published': datetime.datetime.fromisoformat(post_data['date_published']) if post_data.get('date_published') else None,
                'is_featured': post_data.get('is_featured', False),
            }
        )
        
        # Add categories
        if created and 'categories' in post_data:
            for category_name in post_data['categories']:
                if category_name in blog_categories:
                    post.categories.add(blog_categories[category_name])
        
        # Add related projects
        if created and 'related_projects' in post_data:
            for project_name in post_data['related_projects']:
                if project_name in projects:
                    post.related_projects.add(projects[project_name])
        
        # Add related skills
        if created and 'related_skills' in post_data:
            for skill_name in post_data['related_skills']:
                if skill_name in skills:
                    post.related_skills.add(skills[skill_name])
        
        if created:
            print(f"Created BlogPost: {post.title}")
            # Create placeholder image
            create_placeholder_image(post, 'featured_image', f"{slugify(post.title)}_featured.jpg")
    
    print("Data import completed successfully!")

if __name__ == "__main__":
    import_data()