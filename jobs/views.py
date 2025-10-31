from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from .models import Job, JobApplication
from core.models import User, Company
from .serializers import JobSerializer, JobApplicationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_jobs(request):
    jobs = Job.objects.filter(is_approved=True)
    
    # Search functionality
    search = request.GET.get('search', '')
    if search:
        jobs = jobs.filter(
            models.Q(title__icontains=search) |
            models.Q(description__icontains=search) |
            models.Q(company__name__icontains=search)
        )
    
    # Filter by job type
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    # Filter by company
    company_id = request.GET.get('company', '')
    if company_id:
        jobs = jobs.filter(company__id=company_id)
    
    # Order by most recent
    jobs = jobs.order_by('-posted_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    try:
        page = int(page)
        page_size = int(page_size)
        page_size = min(page_size, 50)  # Max 50 items per page
    except ValueError:
        page = 1
        page_size = 10
    
    paginator = Paginator(jobs, page_size)
    jobs_page = paginator.get_page(page)
    
    serializer = JobSerializer(jobs_page, many=True)
    
    return Response({
        'results': serializer.data,
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page,
        'page_size': page_size,
        'has_next': jobs_page.has_next(),
        'has_previous': jobs_page.has_previous()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    serializer = JobSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    user = get_object_or_404(User, pk=user.pk)
    
    # Only employers can create jobs
    if user.is_employer:
        # Get the company associated with this employer
        try:
            company = Company.objects.get(employer=user)
        except Company.DoesNotExist:
            return Response(data={"message": "Company not found. Please create a company first."}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        Job.objects.create(
            company=company,
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            job_type=serializer.validated_data.get('job_type', 'Full-time'),
            location=serializer.validated_data.get('location', ''),
            is_approved=serializer.validated_data.get('is_approved', False),
            deadline=serializer.validated_data.get('deadline', None)
        )
        return Response(data={"message": "job created"}, status=status.HTTP_201_CREATED)
    
    return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    serializer = JobSerializer(job)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    serializer = JobSerializer(job, data=request.data, partial=True)
    
    if serializer.is_valid():
        # Only the employer who created the job or admin can update it
        if (request.user.is_employer and job.company.employer == request.user) or request.user.is_staff:
            serializer.save()
            return Response(serializer.data)
        return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    # Only the employer who created the job or admin can delete it
    if (request.user.is_employer and job.company.employer == request.user) or request.user.is_staff:
        job.delete()
        return Response(data={"message": "job deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)


# Job Application Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    # Check if job is approved
    if not job.is_approved:
        return Response({"message": "Job is not approved yet"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already applied
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        return Response({"message": "Already applied for this job"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if deadline has passed
    if job.deadline and timezone.now() > job.deadline:
        return Response({"message": "Application deadline has passed"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = JobApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    application = JobApplication.objects.create(
        job=job,
        applicant=request.user,
        cover_letter=serializer.validated_data.get('cover_letter', ''),
        resume=serializer.validated_data.get('resume', None)
    )
    
    response_serializer = JobApplicationSerializer(application)
    return Response({"message": "Application submitted successfully", "application": response_serializer.data}, 
                   status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user)
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_applications(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    
    # Only employer who posted the job or admin can view applications
    if not (job.company.employer == request.user or request.user.is_staff):
        return Response({"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    applications = JobApplication.objects.filter(job=job)
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def review_application(request, application_id):
    application = get_object_or_404(JobApplication, pk=application_id)
    
    # Only employer who posted the job or admin can review applications
    if not (application.job.company.employer == request.user or request.user.is_staff):
        return Response({"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    status_value = request.data.get('status')
    if status_value not in ['pending', 'reviewed', 'shortlisted', 'rejected', 'hired']:
        return Response({"message": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
    
    application.status = status_value
    application.reviewed_at = timezone.now()
    application.save()
    
    serializer = JobApplicationSerializer(application)
    return Response(serializer.data)