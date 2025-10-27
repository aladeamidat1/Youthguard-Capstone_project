import uuid
from decimal import Decimal

from django.db import models

from core.models import User


# Create your models here.
class MicroTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_microtasks')  # employer
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=50, blank=True)
    reward = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title


class TaskSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(MicroTask, on_delete=models.PROTECT, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='task_submissions')
    submission = models.TextField(blank=True)  # or FileField if file uploads
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending')
    submitted_at = models.DateTimeField()


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=[('credit','Credit'),('debit','Debit')])
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

