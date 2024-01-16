from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Course
from api.permissions import IsAuthorOrReadOnly
from api.serializers import CourseSerializer

# Create your views here.
class Courses(APIView):
    model = Course
    permission_classes = [IsAuthenticated]

    def _filter_queryset(self, filter_params: dict):
        for param in filter_params.keys():
            if param != 'format' and not hasattr(Course, param):
                raise AttributeError(f"Course object has no attribute called {param}")
        
        for key, value in filter_params.items():
            filter_params[key] = value[0]
        print(filter_params)

        if filter_params.get('price', None) != None:
            filter_params['price'] = float(filter_params['price'])
        if filter_params.get('duration', None) != None:
            filter_params['duration'] = int(filter_params['duration'])


        return self.model.objects.filter(**filter_params)

    def get(self, request, format=None, *args, **kwargs):
        print(f'Request from: {request.user}')
        filter_params = dict(request.query_params)
        if filter_params.get('format', None) != None:
            format = filter_params.pop('format')
            
        queryset = self._filter_queryset(filter_params)
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
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get(self, request, course_slug, format=None, *args, **kwargs):
        course = get_object_or_404(self.model, slug_title=course_slug)
        course = CourseSerializer(course)
        return Response(course.data, status=status.HTTP_200_OK)
        
    def patch(self, request, course_slug, format=None, *args, **kwargs):
        request.data['author'] = request.user.pk
        course = get_object_or_404(self.model, slug_title=course_slug)
        course = CourseSerializer(course, data=request.data, partial=True)
        if course.is_valid():
            course.save()
            print('Course updated')
            return Response(course.data, status=status.HTTP_200_OK)
        
        return Response(course.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, course_slug, format=None, *args, **kwargs):
        course = get_object_or_404(self.model, slug_title=course_slug)
        course.delete()
        return Response({
            'message': 'Course deleted.'
        }, status=status.HTTP_204_NO_CONTENT)
        
all_courses = Courses.as_view()
single_course = ReadUpdateDeleteCourse.as_view()