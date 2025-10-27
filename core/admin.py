from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from django.contrib.auth.models import User

from core.models import User, Company


# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_employer' , 'is_facilitator' , 'phone')
    list_editable = ('is_facilitator', 'is_employer')
    list_display_links = ('email', 'first_name', 'last_name')
    add_fieldsets = (
        (
            None,

            {
                'classes': ('wide',),
                "fields": ('email', 'first_name', 'last_name', 'password1', 'password2','phone')

            }
        )
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name' , 'description', 'employer')

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description' , 'facilitator' , 'is_approved' , 'created_at')
#
#
# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ('company' , 'title' , 'description' , 'created_at' , 'is_approved' )