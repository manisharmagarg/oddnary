from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from utils.base_model import BaseModel
from utils.upload_location import course_file_location
# Create your models here.

User = get_user_model()


class Course(BaseModel):
    author = models.ForeignKey(User, related_name='courses', null=True, 
                            on_delete=models.SET_NULL)
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), null=True, blank=True)
    is_active = models.BooleanField(_('is_active'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    def __str__(self):
        return "{}".format(self.name)

    @property
    def course_sections(self):
        return CourseSection.objects.filter(course_id=self.id)

    class Meta:
        ordering = ('-created_at',)


class CourseSection(BaseModel):
    course = models.ForeignKey(Course, related_name='sections')
    name = models.CharField(_('name'), max_length=256)
    index = models.PositiveIntegerField(_('index'), default=0, blank=True)
    is_active = models.BooleanField(_('is_active'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    def __str__(self):
        return "{} - {}".format(self.index, self.name)

    @property
    def course_files(self):
        return CourseFile.objects.filter(section_id=self.id)

    class Meta:
        ordering = ('course', 'index',)


class CourseFile(BaseModel):
    section = models.ForeignKey(CourseSection, related_name='files')
    name = models.CharField(_('name'), max_length=256)
    description = models.TextField(_('description'), null=True, blank=True)
    file = models.FileField(_('file'), max_length=2048, upload_to=course_file_location)
    index = models.PositiveIntegerField(_('index'), default=0, blank=True)
    is_active = models.BooleanField(_('is_active'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    def __str__(self):
        return "{} - {}".format(self.index, self.name)

    class Meta:
        ordering = ('section', 'index',)


class CourseDetailTab(BaseModel):
    course = models.ForeignKey(Course, related_name='detail_tabs')
    name = models.CharField(_('name'), max_length=64)
    content = models.TextField(_('content'), null=True, blank=True)
    index = models.PositiveIntegerField(_('index'), default=0, blank=True)
    is_active = models.BooleanField(_('is_active'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    def __str__(self):
        return "{} - {}".format(self.course, self.name)

    class Meta:
        ordering = ('course', 'index',)


class CourseDetailTabList(BaseModel):
    course_detail_tab = models.ForeignKey(CourseDetailTab, related_name='lists')
    content = models.TextField(_('content'))
    index = models.PositiveIntegerField(_('index'), default=0, blank=True)
    is_active = models.BooleanField(_('is_active'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    def __str__(self):
        return "{}".format(self.course_detail_tab)

    class Meta:
        ordering = ('course_detail_tab', 'index',)


class UserMyCourseLibrary(BaseModel):
    user = models.ForeignKey(User, related_name='my_course')
    course = models.ForeignKey(Course, related_name='my_course_users')

    def __str__(self):
        return "{} - {}".format(self.user, self.course)

    class Meta:
        ordering = ('-created_at',)


class Category(BaseModel):
    name = models.CharField(_('name'), max_length=64, unique=True)
    description = models.TextField(_('description'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)


class CategoryCourseRelation(BaseModel):
    course = models.ForeignKey(Course, related_name='course_category')
    category = models.ForeignKey(Category, related_name='category_courses')

    def __str__(self):
        return "{} - {}".format(self.category, self.course)

    class Meta:
        ordering = ('-created_at',)