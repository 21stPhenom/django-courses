from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Course
from api.permissions import IsAuthorOrReadOnly
from api.serializers import CourseSerializer

# Create your views here.
class Courses(APIView):
    model = Course
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, *args, **kwargs):
        print(f'Request from: {request.user}')
        queryset = self.model.objects.all()
        queryset = CourseSerializer(queryset, many=True)
        return Response(queryset.data, status=status.HTTP_200_OK)

    def post(self, request, format=None, *args, **kwargs):
        request.data['author'] = request.user.pk
        new_course = CourseSerializer(data=request.data)
        if new_course.is_valid():
            new_course.save()
            return Response(new_course.data, status=status.HTTP_201_CREATED)
        
        return Response(new_course.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReadUpdateDeleteCourse(APIView):
    model = Course
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get(self, request, course_slug, format=None, *args, **kwargs):
        course = get_object_or_404(self.model, slug_title=course_slug)
        serialized_course = CourseSerializer(course)
        return Response(serialized_course.data, status=status.HTTP_200_OK)
        
    def put(self, request, course_slug, format=None, *args, **kwargs):
        request.data['author'] = request.user.pk
        course = get_object_or_404(self.model, slug_title=course_slug)
        serialized_course = CourseSerializer(course, data=request.data)
        if serialized_course.is_valid():
            serialized_course.save()
            print('Course updated')
            return Response(serialized_course.data, status=status.HTTP_200_OK)
        
        return Response(serialized_course.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, course_slug, format=None, *args, **kwargs):
        print(f'Request from: {request.user}')
        course = get_object_or_404(self.model, slug_title=course_slug)
        course.delete()
        return Response({
            'message': 'Course deleted.'
        }, status=status.HTTP_204_NO_CONTENT)
        

all_courses = Courses.as_view()
single_course = ReadUpdateDeleteCourse.as_view()