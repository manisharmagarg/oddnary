from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from utils.base_model import BaseModel
from utils.upload_location import (
    assignment_file_location,
    assignment_solution_file_location
)
from courses.models import (
    Course, CourseSection,
)
# Create your models here.

User = get_user_model()

class Assignment(BaseModel):
    course = models.ForeignKey(Course, related_name='assignments')
    course_section = models.ForeignKey(CourseSection, related_name='assignments',
                                        null=True, blank=True)
    name = models.CharField(_('name'), max_length=512)
    description = models.TextField(_('description'), null=True, blank=True)
    index = models.IntegerField(_('index'), default=0, blank=True)    
    is_active = models.BooleanField(_('is_active'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    def __str__(self):
        return "{} - {}".format(self.course, self.name)

    class Meta:
        ordering = ('course', 'index', '-created_at',)


class AssignmentFile(BaseModel):
    assignment = models.ForeignKey(Assignment, related_name='files')
    name = models.CharField(_('name'), max_length=512)
    file = models.FileField(_('file'), max_length=2048, upload_to=assignment_file_location)
    description = models.TextField(_('description'), null=True, blank=True)
    index = models.IntegerField(_('index'), default=0, blank=True)    
    is_active = models.BooleanField(_('is_active'), default=False)
    is_deleted = models.BooleanField(_('is_deleted'), default=False)

    def __str__(self):
        return "{} - {}".format(self.assignment, self.name)

    class Meta:
        ordering = ('assignment', 'index', '-created_at',)

    
class AssignmentSolution(BaseModel):
    assignment = models.ForeignKey(Assignment, related_name='solutions')
    user = models.ForeignKey(User, related_name='assignment_solutions',)
    comment = models.TextField(null=True, blank=False)

    def __str__(self):
        return "{}".format(self.assignment)


class AssignmentSolutionFile(BaseModel):
    assignment_solution = models.ForeignKey(AssignmentSolution, related_name='files')
    name = models.CharField(max_length=128, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    file = models.FileField(_('file'), max_length=2048, upload_to=assignment_solution_file_location)

    def __str__(self):
        return "{} - {}".format(self.assignment_solution, self.name)


