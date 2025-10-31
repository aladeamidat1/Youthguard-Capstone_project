import uuid

from django.db import models

from core.models import Company


# Create your models here.
class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT , related_name='jobs')
    title = models.CharField(max_length=225, blank= False)
    description = models.TextField(blank= True)
    job_type = models.CharField(
        max_length=20,
        choices=[
            ('Full-time', 'Full-time'),
            ('Part-time', 'Part-time'),
            ('Contract', 'Contract'),
            ('Internship', 'Internship')
        ],
        default='Full-time'
    )
    location = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank= True, null= True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('reviewed', 'Reviewed'),
            ('shortlisted', 'Shortlisted'),
            ('rejected', 'Rejected'),
            ('hired', 'Hired')
        ],
        default='pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('job', 'applicant')  # Prevent duplicate applications

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"
