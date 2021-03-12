# Django imports
from django.conf.urls import url, include

# Local imports
from .views import (
    AssignmentCreateAPIView,
    AssignmentUpdateApiView,
    AssignmentFileCreateAPIView,
    AssignmentFileUpdateApiView,
    )

urlpatterns = [
    url(
        r'^assignment-create/$',
        AssignmentCreateAPIView.as_view(),
        name='admin_assignment_create',
    ),
    url(
        r'^assignment/(?P<pk>[0-9a-z-]+)/$',
        AssignmentUpdateApiView.as_view(),
        name='admin_assignment_update',
    ),
    url(
        r'^assignment-file-create/$',
        AssignmentFileCreateAPIView.as_view(),
        name='assignment_file_create',
    ),
    url(
        r'^assignment-file/(?P<pk>[0-9a-z-]+)/$',
        AssignmentFileUpdateApiView.as_view(),
        name='assignment_file_update',
    ),
]