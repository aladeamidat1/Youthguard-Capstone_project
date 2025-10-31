from django.urls import path
from .views import (
    list_jobs, create_job, get_job, update_job, delete_job,
    apply_for_job, my_applications, job_applications, review_application
)

urlpatterns = [
    path('', list_jobs, name='list-jobs'),
    path('create/', create_job, name='create-job'),
    path('<uuid:job_id>/', get_job, name='get-job'),
    path('<uuid:job_id>/update/', update_job, name='update-job'),
    path('<uuid:job_id>/delete/', delete_job, name='delete-job'),
    
    # Application endpoints
    path('<uuid:job_id>/apply/', apply_for_job, name='apply-for-job'),
    path('my-applications/', my_applications, name='my-applications'),
    path('<uuid:job_id>/applications/', job_applications, name='job-applications'),
    path('applications/<uuid:application_id>/review/', review_application, name='review-application'),
]