

from django.urls import path
from .views import (
    current_user, create_company, create_user, user_profile, get_user_profile,
    list_companies, get_company, update_company, delete_company, register_with_role,
    dashboard_stats
)

urlpatterns = [
    path('register/', create_user, name='create-user'),
    path('register-with-role/', register_with_role, name='register-with-role'),
    path('current-user/', current_user, name='current-user'),
    path('create-company/', create_company, name='create-company'),
    
    # Profile endpoints
    path('profile/', user_profile, name='user-profile'),
    path('profile/<uuid:user_id>/', get_user_profile, name='get-user-profile'),
    
    # Company endpoints
    path('companies/', list_companies, name='list-companies'),
    path('companies/<uuid:company_id>/', get_company, name='get-company'),
    path('companies/<uuid:company_id>/update/', update_company, name='update-company'),
    path('companies/<uuid:company_id>/delete/', delete_company, name='delete-company'),
    
    # Dashboard endpoints
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
]