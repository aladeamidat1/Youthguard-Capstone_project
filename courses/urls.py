from django.urls import path
from .views import list_courses, create_course, get_course, update_course, delete_course

urlpatterns = [
    path('', list_courses, name='list-courses'),

    path('create/', create_course, name='create-course'),

    path('<uuid:course_id>/', get_course, name='get-course'),

    path('<uuid:course_id>/update/', update_course, name='update-course'),

    path('<uuid:course_id>/delete/', delete_course, name='delete-course'),
]