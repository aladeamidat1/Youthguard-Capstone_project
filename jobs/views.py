from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from core.models import User, Company
from .serializers import JobSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


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