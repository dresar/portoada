from django import forms
from .models import (
    Profile, Skill, Project, Experience, Certificate, 
    Contact, Service, Testimonial, Blog, Award, PortfolioSettings as Settings,
    BlogCategory, BlogTag, BlogComment
)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = '__all__'

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogTagForm(forms.ModelForm):
    class Meta:
        model = BlogTag
        fields = '__all__'

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = '__all__'