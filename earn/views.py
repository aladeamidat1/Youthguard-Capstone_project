from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import MicroTask, TaskSubmission, Wallet, Transaction
from core.models import User
from .serializers import MicroTaskSerializer, TaskSubmissionSerializer, WalletSerializer, TransactionSerializer


# MicroTask Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tasks(request):
    tasks = MicroTask.objects.filter(is_active=True)
    
    # Search functionality
    search = request.GET.get('search', '')
    if search:
        tasks = tasks.filter(
            models.Q(title__icontains=search) |
            models.Q(description__icontains=search)
        )
    
    # Filter by task type
    task_type = request.GET.get('task_type', '')
    if task_type:
        tasks = tasks.filter(task_type=task_type)
    
    # Filter by reward range
    min_reward = request.GET.get('min_reward', '')
    max_reward = request.GET.get('max_reward', '')
    
    if min_reward:
        try:
            tasks = tasks.filter(reward__gte=float(min_reward))
        except ValueError:
            pass
    
    if max_reward:
        try:
            tasks = tasks.filter(reward__lte=float(max_reward))
        except ValueError:
            pass
    
    # Order by highest reward first
    tasks = tasks.order_by('-reward', '-created_at')
    
    serializer = MicroTaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = MicroTaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    user = get_object_or_404(User, pk=user.pk)
    
    # Only employers can create tasks
    if user.is_employer:
        MicroTask.objects.create(
            created_by=user,
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            task_type=serializer.validated_data.get('task_type', ''),
            reward=serializer.validated_data['reward'],
            is_active=serializer.validated_data.get('is_active', True)
        )
        return Response(data={"message": "task created"}, status=status.HTTP_201_CREATED)
    
    return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request, task_id):
    task = get_object_or_404(MicroTask, pk=task_id)
    serializer = MicroTaskSerializer(task)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    task = get_object_or_404(MicroTask, pk=task_id)
    serializer = MicroTaskSerializer(task, data=request.data, partial=True)
    
    if serializer.is_valid():
        # Only the employer who created the task or admin can update it
        if (request.user.is_employer and task.created_by == request.user) or request.user.is_staff:
            serializer.save()
            return Response(serializer.data)
        return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    task = get_object_or_404(MicroTask, pk=task_id)
    
    # Only the employer who created the task or admin can delete it
    if (request.user.is_employer and task.created_by == request.user) or request.user.is_staff:
        task.delete()
        return Response(data={"message": "task deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)


# Task Submission Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_task(request, task_id):
    task = get_object_or_404(MicroTask, pk=task_id)
    serializer = TaskSubmissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    
    # Anyone can submit a task (assuming learners/users)
    TaskSubmission.objects.create(
        task=task,
        user=user,
        submission=serializer.validated_data['submission'],
        status='pending'
    )
    
    return Response(data={"message": "task submitted"}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def review_submission(request, submission_id):
    submission = get_object_or_404(TaskSubmission, pk=submission_id)
    serializer = TaskSubmissionSerializer(submission, data=request.data, partial=True)
    
    if serializer.is_valid():
        # Only the employer who created the task or admin can review submissions
        if (request.user.is_employer and submission.task.created_by == request.user) or request.user.is_staff:
            old_status = submission.status
            serializer.save()
            
            # If the submission is approved, update the user's wallet
            if old_status != 'approved' and submission.status == 'approved':
                # Get or create wallet for the user
                wallet, created = Wallet.objects.get_or_create(user=submission.user)
                
                # Add reward to wallet
                wallet.balance += submission.task.reward
                wallet.save()
                
                # Create transaction record
                Transaction.objects.create(
                    wallet=wallet,
                    amount=submission.task.reward,
                    type='credit',
                    description=f'Earnings from task: {submission.task.title}'
                )
            
            return Response(serializer.data)
        return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Wallet Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_to_wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    serializer = WalletSerializer(wallet, data=request.data, partial=True)
    
    if serializer.is_valid():
        amount = request.data.get('amount', 0)
        if amount > 0:
            wallet.balance += amount
            wallet.save()
            
            # Create transaction record
            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                type='credit',
                description='Deposit'
            )
            
            return Response(data={"message": f"Successfully deposited {amount}", "balance": wallet.balance})
        
        return Response(data={"message": "Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Transaction Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transactions(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(wallet=wallet)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_submissions(request):
    submissions = TaskSubmission.objects.filter(user=request.user)
    serializer = TaskSubmissionSerializer(submissions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_from_wallet(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    amount = request.data.get('amount', 0)
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return Response({"message": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)
    
    if amount <= 0:
        return Response({"message": "Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
    
    if wallet.balance < amount:
        return Response({"message": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Minimum withdrawal amount
    if amount < 5.00:
        return Response({"message": "Minimum withdrawal amount is $5.00"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Process withdrawal
    wallet.balance -= amount
    wallet.save()
    
    # Create transaction record
    Transaction.objects.create(
        wallet=wallet,
        amount=amount,
        type='debit',
        description=f'Withdrawal to bank account'
    )
    
    return Response({
        "message": f"Successfully withdrew ${amount}",
        "new_balance": wallet.balance,
        "withdrawal_amount": amount
    }, status=status.HTTP_200_OK)