from django.shortcuts import render


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer
from core.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_courses(request):
    courses = Course.objects.all()
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
# Create your views here.
