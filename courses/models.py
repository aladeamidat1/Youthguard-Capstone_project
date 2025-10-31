import uuid


from django.db import models

from core.models import User


# Create your models here.

class Course(models.Model):
    id = models.UUIDField(primary_key=True ,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=225, blank= False)
    description = models.TextField(blank= False)
    facilitator = models.ForeignKey(User, on_delete=models.PROTECT , related_name='facilitator_courses')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class CourseEnrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)  # Progress percentage (0-100)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('course', 'learner')  # Prevent duplicate enrollments

    def __str__(self):
        return f"{self.learner.username} enrolled in {self.course.name}"

