from django.contrib import admin
from .models import Job, JobApplication

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'is_approved', 'created_at', 'deadline')
    list_filter = ('is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('title', 'company__name')
    actions = ['approve_jobs', 'disapprove_jobs']

    def approve_jobs(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} jobs approved.")
    approve_jobs.short_description = "Approve selected jobs"

    def disapprove_jobs(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} jobs disapproved.")
    disapprove_jobs.short_description = "Disapprove selected jobs"

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'applicant__username')
    actions = ['mark_reviewed', 'mark_shortlisted', 'mark_rejected']

    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
        self.message_user(request, f"{queryset.count()} applications marked as reviewed.")
    mark_reviewed.short_description = "Mark as reviewed"

    def mark_shortlisted(self, request, queryset):
        queryset.update(status='shortlisted')
        self.message_user(request, f"{queryset.count()} applications shortlisted.")
    mark_shortlisted.short_description = "Mark as shortlisted"

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} applications rejected.")
    mark_rejected.short_description = "Mark as rejected"
