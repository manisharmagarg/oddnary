# Django Imports
from django.conf.urls import url, include

urlpatterns = [
    url(
        r'^admin/',
        include('courses.api.admin.urls'),
    ),
    url(
        r'^user/',
        include('courses.api.user.urls'),
    ),
    url(
        r'^public/',
        include('courses.api.public.urls'),
    ),
]