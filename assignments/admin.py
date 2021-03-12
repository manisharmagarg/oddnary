from django.contrib import admin

from .models import (
    Assignment, AssignmentFile,
    AssignmentSolution, AssignmentSolutionFile,
)
from utils.admin import CustomAdminFormMixin
# Register your models here.


@admin.register(Assignment)
class AssignmentAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(AssignmentFile)
class AssignmentFileAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(AssignmentSolution)
class AssignmentSolutionAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass


@admin.register(AssignmentSolutionFile)
class AssignmentSolutionFileAdmin(CustomAdminFormMixin, admin.ModelAdmin):
    pass

