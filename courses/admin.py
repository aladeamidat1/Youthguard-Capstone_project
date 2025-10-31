from django.contrib import admin
from .models import Course, CourseEnrollment

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'facilitator', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('name', 'facilitator__username')
    actions = ['approve_courses', 'disapprove_courses']

    def approve_courses(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} courses approved.")
    approve_courses.short_description = "Approve selected courses"

    def disapprove_courses(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f"{queryset.count()} courses disapproved.")
    disapprove_courses.short_description = "Disapprove selected courses"

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'learner', 'progress', 'completed', 'enrolled_at')
    list_filter = ('completed', 'enrolled_at')
    search_fields = ('course__name', 'learner__username')
