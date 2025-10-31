import uuid


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_facilitator = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, blank= False , unique=True , null=True)
    bio = models.TextField(blank= True)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert')
        ],
        default='beginner'
    )
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225, blank= False)
    description = models.TextField(blank= True)
    website = models.URLField(blank=True, null=True)
    employer = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

# class Course(models.Model):
#     name = models.CharField(max_length=225, blank= False)
#     description = models.TextField(blank= False)
#     facilitator = models.ForeignKey(User, on_delete=models.PROTECT , related_name='facilitator_courses')
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

# class Job(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.PROTECT , related_name='jobs')
#     title = models.CharField(max_length=225, blank= False)
#     description = models.TextField(blank= True)
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)


