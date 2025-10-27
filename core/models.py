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



class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225, blank= False)
    description = models.TextField(blank= True)
    employer = models.ForeignKey(User, on_delete=models.PROTECT)

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


