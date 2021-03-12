from django.contrib import admin

from .models import (
    Course, CourseSection,
    CourseFile, CourseDetailTab,
    CourseDetailTabList,
    UserMyCourseLibrary,
    Category,
    CategoryCourseRelation,
)
from utils.admin import CustomAdminFormMixin
# Register your models here.

@admin.register(Course)
class CourseAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(CourseSection)
class CourseSectionAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(CourseFile)
class CourseFileAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(CourseDetailTab)
class CourseDetailTabAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(CourseDetailTabList)
class CourseDetailTabListAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(UserMyCourseLibrary)
class UserMyCourseLibraryAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(Category)
class CourseAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(CategoryCourseRelation)
class CourseAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass