from django.urls import path
from .views import (
    list_courses, create_course, get_course, update_course, delete_course,
    enroll_in_course, my_enrollments, update_progress, course_enrollments
)

urlpatterns = [
    path('', list_courses, name='list-courses'),
    path('create/', create_course, name='create-course'),
    path('<uuid:course_id>/', get_course, name='get-course'),
    path('<uuid:course_id>/update/', update_course, name='update-course'),
    path('<uuid:course_id>/delete/', delete_course, name='delete-course'),
    
    # Enrollment endpoints
    path('<uuid:course_id>/enroll/', enroll_in_course, name='enroll-in-course'),
    path('my-enrollments/', my_enrollments, name='my-enrollments'),
    path('enrollments/<uuid:enrollment_id>/progress/', update_progress, name='update-progress'),
    path('<uuid:course_id>/enrollments/', course_enrollments, name='course-enrollments'),
]