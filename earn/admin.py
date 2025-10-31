from django.contrib import admin
from .models import MicroTask, TaskSubmission, Wallet, Transaction

# Register your models here.

@admin.register(MicroTask)
class MicroTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'reward', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'task_type')
    search_fields = ('title', 'created_by__username')

@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    list_editable = ('status',)
    search_fields = ('task__title', 'user__username')
    actions = ['approve_submissions', 'reject_submissions']

    def approve_submissions(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} submissions approved.")
    approve_submissions.short_description = "Approve selected submissions"

    def reject_submissions(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} submissions rejected.")
    reject_submissions.short_description = "Reject selected submissions"

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'type', 'timestamp', 'description')
    list_filter = ('type', 'timestamp')
    search_fields = ('wallet__user__username', 'description')
