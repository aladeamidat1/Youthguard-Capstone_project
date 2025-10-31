from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Course, CourseEnrollment
from .serializers import CourseSerializer, CourseEnrollmentSerializer
from core.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_courses(request):
    courses = Course.objects.filter(is_approved=True)
    
    # Search functionality
    search = request.GET.get('search', '')
    if search:
        courses = courses.filter(
            models.Q(name__icontains=search) |
            models.Q(description__icontains=search)
        )
    
    # Filter by facilitator
    facilitator_id = request.GET.get('facilitator', '')
    if facilitator_id:
        courses = courses.filter(facilitator__id=facilitator_id)
    
    # Order by most recent
    courses = courses.order_by('-created_at')
    
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    user = get_object_or_404(User, pk=user.pk)
    
    # Only facilitators can create courses
    if user.is_facilitator:
        Course.objects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            facilitator=user,
            is_approved=serializer.validated_data.get('is_approved', False)
        )
        return Response(data={"message": "course created"}, status=status.HTTP_201_CREATED)
    
    return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    serializer = CourseSerializer(course, data=request.data, partial=True)
    
    if serializer.is_valid():
        # Only the facilitator or admin can update the course
        if request.user.is_facilitator and course.facilitator == request.user or request.user.is_staff:
            serializer.save()
            return Response(serializer.data)
        return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Only the facilitator or admin can delete the course
    if request.user.is_facilitator and course.facilitator == request.user or request.user.is_staff:
        course.delete()
        return Response(data={"message": "course deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    return Response(data={"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)


# Course Enrollment Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Check if course is approved
    if not course.is_approved:
        return Response({"message": "Course is not approved yet"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user is already enrolled
    if CourseEnrollment.objects.filter(course=course, learner=request.user).exists():
        return Response({"message": "Already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create enrollment
    enrollment = CourseEnrollment.objects.create(
        course=course,
        learner=request.user
    )
    
    serializer = CourseEnrollmentSerializer(enrollment)
    return Response({"message": "Successfully enrolled", "enrollment": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_enrollments(request):
    enrollments = CourseEnrollment.objects.filter(learner=request.user)
    serializer = CourseEnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_progress(request, enrollment_id):
    enrollment = get_object_or_404(CourseEnrollment, pk=enrollment_id, learner=request.user)
    
    progress = request.data.get('progress', enrollment.progress)
    if progress == 100 and not enrollment.completed:
        enrollment.completed = True
        enrollment.completed_at = timezone.now()
    
    enrollment.progress = progress
    enrollment.save()
    
    serializer = CourseEnrollmentSerializer(enrollment)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_enrollments(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Only facilitator of the course or admin can view enrollments
    if not (course.facilitator == request.user or request.user.is_staff):
        return Response({"message": "Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    enrollments = CourseEnrollment.objects.filter(course=course)
    serializer = CourseEnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)
