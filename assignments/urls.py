# Django Imports
from django.conf.urls import url, include

urlpatterns = [
    url(
        r'^admin/',
        include('assignments.api.admin.urls'),
    ),
    url(
        r'^user/',
        include('assignments.api.user.urls'),
    ),
]