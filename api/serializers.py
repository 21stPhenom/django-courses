from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
