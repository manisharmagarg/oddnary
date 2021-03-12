# restframework imports
from rest_framework import serializers
# djnago imports
from django.contrib.auth import get_user_model

# Local Imports
from assignments.models import (
    Assignment,
    AssignmentFile,
    )
from courses.models import (
    Course,
    CourseSection,
    )
User = get_user_model()


class AssignmentCreateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True
        )
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    index = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField(required=False)
    
    class Meta:
        model = Assignment
        fields = [
            'course',
            'course_section',
            'name',
            'description',
            'index',
            'is_active',
        ]


class AssignmentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assignment
        fields = [
            'course',
            'course_section',
            'name',
            'description',
            'index',
            'is_active',
        ]


class AssignmentFileCreateSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all(),
        required=True
        )
    name = serializers.CharField(required=True)
    file = serializers.FileField(
        allow_empty_file=False,
        max_length=2048
        )
    description = serializers.CharField(required=True)
    index = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField(required=False)
    
    class Meta:
        model = AssignmentFile
        fields = [
            'assignment',
            'name',
            'file',
            'description',
            'index',
            'is_active',
        ]


class AssignmentFilleUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AssignmentFile
        fields = [
            'assignment',
            'name',
            'file',
            'description',
            'index',
            'is_active',
        ]