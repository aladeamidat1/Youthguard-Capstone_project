from django.urls import path
from .views import list_jobs, create_job, get_job, update_job, delete_job

urlpatterns = [
    path('', list_jobs, name='list-jobs'),

    path('create/', create_job, name='create-job'),

    path('<uuid:job_id>/', get_job, name='get-job'),

    path('<uuid:job_id>/update/', update_job, name='update-job'),

    path('<uuid:job_id>/delete/', delete_job, name='delete-job'),
]