from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Company, UserProfile
from .serializers import UserCreateSerializer, CompanySerializer, UserProfileSerializer

User = get_user_model()


# Create User (Registration)
User = get_user_model()

@api_view(['POST'])
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User created successfully", "user": serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ✅ 2. Get Current Logged-in User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserCreateSerializer(request.user)
    return Response(serializer.data)


# ✅ 3. Create Company (Only Employers)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_company(request):
    serializer = CompanySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user  # already the logged-in user

    # Only employers can create companies
    if getattr(user, "is_employer", False):  # prevent attribute error if field missing
        Company.objects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            employer=user
        )
        return Response({"message": "Company created"}, status=status.HTTP_201_CREATED)

    return Response({"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)


# User Profile Views
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_with_role(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Set role based on request data
        role = request.data.get('role', 'Learner')
        if role == 'Facilitator':
            user.is_facilitator = True
        elif role == 'Employer':
            user.is_employer = True
        # Learner is default (no special flags)
        
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return Response(
            {"message": "User created successfully", "user": serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


# Company Management Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_companies(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    serializer = CompanySerializer(company)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    
    # Only company owner or admin can update
    if not (company.employer == request.user or request.user.is_staff):
        return Response({"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CompanySerializer(company, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    
    # Only company owner or admin can delete
    if not (company.employer == request.user or request.user.is_staff):
        return Response({"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    company.delete()
    return Response({"message": "Company deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Dashboard Statistics
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    stats = {}
    
    if user.is_staff:  # Admin
        from courses.models import Course, CourseEnrollment
        from jobs.models import Job, JobApplication
        from earn.models import MicroTask, TaskSubmission
        
        stats = {
            'total_users': User.objects.count(),
            'total_courses': Course.objects.count(),
            'total_jobs': Job.objects.count(),
            'total_tasks': MicroTask.objects.count(),
            'pending_course_approvals': Course.objects.filter(is_approved=False).count(),
            'pending_job_approvals': Job.objects.filter(is_approved=False).count(),
            'total_enrollments': CourseEnrollment.objects.count(),
            'total_applications': JobApplication.objects.count(),
            'total_submissions': TaskSubmission.objects.count(),
        }
    
    elif user.is_facilitator:
        from courses.models import Course, CourseEnrollment
        
        user_courses = Course.objects.filter(facilitator=user)
        stats = {
            'my_courses': user_courses.count(),
            'approved_courses': user_courses.filter(is_approved=True).count(),
            'pending_courses': user_courses.filter(is_approved=False).count(),
            'total_enrollments': CourseEnrollment.objects.filter(course__facilitator=user).count(),
        }
    
    elif user.is_employer:
        from jobs.models import Job, JobApplication
        from earn.models import MicroTask, TaskSubmission
        
        user_companies = Company.objects.filter(employer=user)
        user_jobs = Job.objects.filter(company__employer=user)
        user_tasks = MicroTask.objects.filter(created_by=user)
        
        stats = {
            'my_companies': user_companies.count(),
            'my_jobs': user_jobs.count(),
            'approved_jobs': user_jobs.filter(is_approved=True).count(),
            'pending_jobs': user_jobs.filter(is_approved=False).count(),
            'total_applications': JobApplication.objects.filter(job__company__employer=user).count(),
            'my_tasks': user_tasks.count(),
            'active_tasks': user_tasks.filter(is_active=True).count(),
            'total_task_submissions': TaskSubmission.objects.filter(task__created_by=user).count(),
        }
    
    else:  # Learner
        from courses.models import CourseEnrollment
        from jobs.models import JobApplication
        from earn.models import TaskSubmission, Wallet
        
        wallet, created = Wallet.objects.get_or_create(user=user)
        
        stats = {
            'my_enrollments': CourseEnrollment.objects.filter(learner=user).count(),
            'completed_courses': CourseEnrollment.objects.filter(learner=user, completed=True).count(),
            'my_applications': JobApplication.objects.filter(applicant=user).count(),
            'my_submissions': TaskSubmission.objects.filter(user=user).count(),
            'approved_submissions': TaskSubmission.objects.filter(user=user, status='approved').count(),
            'wallet_balance': float(wallet.balance),
        }
    
    return Response(stats)
