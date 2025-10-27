import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Course(models.Model):
    id = models.UUIDField(primary_key=True ,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=225, blank= False)
    description = models.TextField(blank= False)
    facilitator = models.ForeignKey(User, on_delete=models.PROTECT , related_name='facilitator_courses')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField

    def __str__(self):
        return self.title

