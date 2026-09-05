from django.contrib import admin
from .models import (
    Profile, About, Education, Skill, Project, Experience,
    Certificate, Contact, Service, Testimonial, Blog, Award,
    BlogCategory, BlogTag, BlogComment, SocialMedia, PortfolioSettings
)

# Register models to admin
admin.site.register(Profile)
admin.site.register(About)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Experience)
admin.site.register(Certificate)
admin.site.register(Contact)
admin.site.register(Service)
admin.site.register(Testimonial)
admin.site.register(Blog)
admin.site.register(Award)
admin.site.register(BlogCategory)
admin.site.register(BlogTag)
admin.site.register(BlogComment)
admin.site.register(SocialMedia)
admin.site.register(PortfolioSettings)
