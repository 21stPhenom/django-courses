from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_title(self, value):
        print("Error from here")
        if Course.objects.filter(title=value).exists():
            raise serializers.ValidationError("This field must be unique")
        return value
