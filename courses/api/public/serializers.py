# restframework imports
from rest_framework import serializers
# djnago imports
from django.contrib.auth import get_user_model

# Local Imports
from courses.models import (
    Course,
    CourseDetailTab,
    CourseDetailTabList,
    CategoryCourseRelation,
    Category,
    )

User = get_user_model()


class PublicCourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
        ]


class CourseDetailTabListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDetailTabList
        fields = [
            'content',
            'index',
        ]


class PublicCourseDetailTabSerializer(serializers.ModelSerializer):
    lists = serializers.SerializerMethodField()

    class Meta:
        model = CourseDetailTab
        fields = [
            'name',
            'content',
            'index',
            'lists',
        ]

    def get_lists(self, obj):
        lists = obj.lists.filter(is_active=True, is_deleted=False)
        serializer = CourseDetailTabListSerializer(lists, many=True)
        return serializer.data


class PublicCourseDetailSerializer(serializers.ModelSerializer):
    tabs = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'tabs',
        ]

    def get_tabs(self, obj):
        tabs = obj.detail_tabs.filter(is_active=True, is_deleted=False)
        serializer = PublicCourseDetailTabSerializer(tabs, many=True)
        return serializer.data


class CategoryCourseSerializer(serializers.ModelSerializer):
    course = PublicCourseListSerializer(read_only=True)

    class Meta:
        model = CategoryCourseRelation
        fields = [
            'id',
            'course',
        ]


class PublicCategoryCourseDetailSerializer(serializers.ModelSerializer):
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