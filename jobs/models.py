import uuid

from django.db import models

from core.models import Company


# Create your models here.
class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT , related_name='jobs')
    title = models.CharField(max_length=225, blank= False)
    description = models.TextField(blank= True)
    is_approved = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank= True, null= True)

    def __str__(self):
        return self.title
