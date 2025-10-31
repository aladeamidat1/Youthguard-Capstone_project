from django.urls import path
from .views import (
    list_tasks, create_task, get_task, update_task, delete_task,
    submit_task, review_submission,
    get_wallet, deposit_to_wallet, withdraw_from_wallet,
    list_transactions, my_submissions
)

urlpatterns = [
    # Task endpoints
    path('tasks/', list_tasks, name='list-tasks'),

    path('tasks/create/', create_task, name='create-task'),

    path('tasks/<uuid:task_id>/', get_task, name='get-task'),

    path('tasks/<uuid:task_id>/update/', update_task, name='update-task'),

    path('tasks/<uuid:task_id>/delete/', delete_task, name='delete-task'),
    
    # Submission endpoints
    path('tasks/<uuid:task_id>/submit/', submit_task, name='submit-task'),

    path('submissions/<uuid:submission_id>/review/', review_submission, name='review-submission'),
    
    # Wallet endpoints
    path('wallet/', get_wallet, name='get-wallet'),
    path('wallet/deposit/', deposit_to_wallet, name='deposit-to-wallet'),
    path('wallet/withdraw/', withdraw_from_wallet, name='withdraw-from-wallet'),
    
    # Transaction endpoints
    path('transactions/', list_transactions, name='list-transactions'),
    
    # Submission endpoints
    path('submissions/', my_submissions, name='my-submissions'),
]