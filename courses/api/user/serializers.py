# restframework imports
from rest_framework import serializers
# djnago imports
from django.contrib.auth import get_user_model

# Local Imports
from courses.models import (
    Course,
    UserMyCourseLibrary,
    Category,
    CategoryCourseRelation,
    )

User = get_user_model()


class UserCourseListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = [
            'name',
            'description',
            'is_active',
        ]

class AddCouserInMyCoursesSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True
        )

    class Meta:
        model = UserMyCourseLibrary
        fields = [
            'course',
        ]


class CategoryCourseSerializer(serializers.ModelSerializer):
    course = UserCourseListSerializer(read_only=True)

    class Meta:
        model = CategoryCourseRelation
        fields = [
            'id',
            'course',
        ]


class UserCategoryCourseDetailSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'courses'
        ]

    def get_courses(self, obj):
        courses = obj.category_courses.all()
        serializer = CategoryCourseSerializer(courses, many=True)
        return serializer.data