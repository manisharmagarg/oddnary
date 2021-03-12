# Django imports
from django.conf.urls import url, include

# Local imports
from .views import (
    AssignmentDetailAPIView,
    CourseAssignmentDetailAPIView,
    AssignmentSolutionCreateAPIView,
    AssignmentSolutionDetailAPIView,
    AssignmentSolutionFileUploadAPIView,
    AssignmentSolutionDetailWithFileAPIView,
    )

urlpatterns = [
    url(
        r'^assignment/(?P<pk>[0-9a-z-]+)/$',
        AssignmentDetailAPIView.as_view(),
        name='user_assignment_detail',
    ),
    url(
        r'^course-assignments/(?P<pk>[0-9a-z-]+)/$',
        CourseAssignmentDetailAPIView.as_view(),
        name='course_assignments_detail',
    ),
    url(
        r'^assignment-solution/$',
        AssignmentSolutionCreateAPIView.as_view(),
        name='assignment_solution_create',
    ),
    url(
        r'^assignment-solution-detail/(?P<pk>[0-9a-z-]+)/$',
        AssignmentSolutionDetailAPIView.as_view(),
        name='assignment_solution_detail',
    ),
    url(
        r'^assignment-solution-all-details/(?P<pk>[0-9a-z-]+)/$',
        AssignmentSolutionDetailWithFileAPIView.as_view(),
        name='assignment_solution_detail_with_file',
    ),
    url(
        r'^assignment-solution-file/$',
        AssignmentSolutionFileUploadAPIView.as_view(),
        name='assignment_solution_file_upload',
    ),
]