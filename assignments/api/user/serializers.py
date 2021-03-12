# restframework imports
from rest_framework import serializers
# djnago imports
from django.contrib.auth import get_user_model

# Local Imports
from assignments.models import (
    Assignment,
    AssignmentFile,
    AssignmentSolution,
    AssignmentSolutionFile,
    )

User = get_user_model()


class AssignmentFileListSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all()
        )
    
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


class AssignmentDetailSerializer(serializers.ModelSerializer):
    files = AssignmentFileListSerializer(
        many=True
        )
    
    class Meta:
        model = Assignment
        fields = [
            'course',
            'course_section',
            'name',
            'description',
            'index',
            'is_active',
            'files',
        ]


class AssignmentSolutionCreateSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(
        queryset=Assignment.objects.all()
        )
    comment = serializers.CharField(required=True)
    
    class Meta:
        model = AssignmentSolution
        fields = [
            'assignment',
            'comment',
        ]


class AssignmentSolutionDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AssignmentSolution
        fields = [
            'comment',
        ]


class AssignmentSolutionFileListSerializer(serializers.ModelSerializer):
    assignment_solution = serializers.PrimaryKeyRelatedField(
        queryset=AssignmentSolution.objects.all()
        )
    
    class Meta:
        model = AssignmentSolutionFile
        fields = [
            'assignment_solution',
            'name',
            'comment',
        ]


class AssignmentSolutionDetailWithFileSerializer(serializers.ModelSerializer):
    files = AssignmentSolutionFileListSerializer(
        many=True
        )
    
    class Meta:
        model = AssignmentSolution
        fields = [
            'comment',
            'files',
        ]


class AssignmentSolutionFileUploadSerializer(serializers.ModelSerializer):
    assignment_solution = serializers.PrimaryKeyRelatedField(
        queryset=AssignmentSolution.objects.all()
        )
    name = serializers.CharField(required=True)
    comment = serializers.CharField(required=True)
    file = serializers.FileField(
        allow_empty_file=False,
        max_length=2048
        )
    
    class Meta:
        model = AssignmentSolutionFile
        fields = [
            'assignment_solution',
            'name',
            'comment',
            'file',
        ]