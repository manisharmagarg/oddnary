# restframework imports
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# djnago imports
from django.contrib.auth import get_user_model

# Local Imports
from courses.models import (
    Course,
    CourseSection,
    CourseFile,
    CourseDetailTab,
    CourseDetailTabList,
    Category,
    CategoryCourseRelation,
    )

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]


class CourseCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id',
            'author',
            'name',
            'description',
            'is_active',
        ]


class CourseSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id',
            'author',
            'name',
            'description',
            'is_active',
            'is_deleted',
        ]


class CourseSectionCreateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True
        )
    name = serializers.CharField(required=True)
    index = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = CourseSection
        fields = [
            'course',
            'name',
            'index',
            'is_active',
        ]


class CourseSectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = CourseSection
        fields = [
            'id',
            'course',
            'name',
            'index',
            'is_active',
        ]


class CourseFileCreateSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(
        queryset=CourseSection.objects.all(),
        required=True
        )
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    file = serializers.FileField(
        allow_empty_file=False,
        max_length=2048
        )
    index = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField(required=False)
    
    class Meta:
        model = CourseFile
        fields = [
            'section',
            'name',
            'description',
            'file',
            'index',
            'is_active',
        ]


class CourseFileSerializer(serializers.ModelSerializer):
    section = CourseSectionSerializer(read_only=True)

    class Meta:
        model = CourseFile
        fields = [
            'id',
            'section',
            'name',
            'description',
            'file',
            'index',
            'is_active',
        ]


class CourseFileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseFile
        fields = [
            'section',
            'name',
            'description',
            'file',
            'index',
            'is_active',
        ]


class CourseSectionListSerializer(serializers.ModelSerializer):
    
    course_files = CourseFileListSerializer(many=True)
    class Meta:
        model = CourseSection
        fields = [
            'course',
            'name',
            'index',
            'is_active',
            'course_files',
        ]


class CoursesDetailSerializer(serializers.ModelSerializer):

    course_sections = CourseSectionListSerializer(many=True)
    class Meta:
        model = Course
        fields = [
            'author',
            'name',
            'description',
            'is_active',
            'course_sections',
        ]


class CourseDetailTabCreateSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True
        )
    name = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    index = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = CourseDetailTab
        fields = [
            'course',
            'name',
            'content',
            'index',
            'is_active',
        ]


class CourseDetailTabSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseDetailTab
        fields = [
            'id',
            'course',
            'name',
            'content',
            'index',
            'is_active',
        ]


class CourseDetailTabListCreateSerializer(serializers.ModelSerializer):
    course_detail_tab = serializers.PrimaryKeyRelatedField(
        queryset=CourseDetailTab.objects.all(),
        required=True
        )
    content = serializers.CharField(required=True)
    index = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField(required=False)


    class Meta:
        model = CourseDetailTabList
        fields = [
            'course_detail_tab',
            'content',
            'index',
            'is_active',
        ]


class CourseDetailTabListDetailSerializer(serializers.ModelSerializer):
    course_detail_tab = CourseDetailTabSerializer(read_only=True)

    class Meta:
        model = CourseDetailTabList
        fields = [
            'id',
            'course_detail_tab',
            'content',
            'index',
            'is_active',
        ]


class CourseFileDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseFile
        fields = [
            'id',
            'name',
            'description',
            'file',
            'index',
            'is_active',
        ]


class CourseSectionDetailSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    class Meta:
        model = CourseSection
        fields = [
            'id',
            'files',
            'name',
            'index',
            'is_active',
        ]

    def get_files(self, obj):
        files = obj.files.all()
        serializer = CourseFileDetailSerializer(files, many=True)
        return serializer.data


class CourseDetailTabListsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDetailTabList
        fields = [
            'id',
            'index',
            'is_active',
        ]


class CourseDetailTabDetailSerializer(serializers.ModelSerializer):
    lists = serializers.SerializerMethodField()

    class Meta:
        model = CourseDetailTab
        fields = [
            'id',
            'lists',
            'name',
            'content',
            'index',
            'is_active',
        ]

    def get_lists(self, obj):
        lists = obj.lists.all()
        serializer = CourseDetailTabListsDetailSerializer(lists, many=True)
        return serializer.data


class CoursesFullDetailSerializer(serializers.ModelSerializer):
    sections = CourseSectionDetailSerializer(many=True)
    detail_tabs = CourseDetailTabDetailSerializer(many=True)
    author = UserSerializer(read_only=True)


    class Meta:
        model = Course
        fields = [
            'id',
            'author',
            'name',
            'description',
            'is_active',
            'sections',
            'detail_tabs',
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(queryset=Category.objects.all())
        ]
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
        ]


class CategoryCourseCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
        )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        required=True
        )

    class Meta:
        model = CategoryCourseRelation
        fields = [
            'id',
            'course',
            'category',
        ]


class CategoryCourseRelationSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CategoryCourseRelation
        fields = [
            'id',
            'course',
            'category',
        ]


class CategoryCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
        ]


class CategoryCourseUpdateSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    category = CategoryCourseSerializer(read_only=True)

    class Meta:
        model = CategoryCourseRelation
        fields = [
            'id',
            'course',
            'category',
        ]
