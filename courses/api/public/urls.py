# Django imports
from django.conf.urls import url, include

# Local imports
from .views import (
    PublicCourseListAPIView,
    PublicCourseDetailAPIView,
    PublicCategoryCourseFullDetailApiView,
    PublicCategoryCourseDetailApiView,

)

urlpatterns = [
    url(
        r'^courses/$',
        PublicCourseListAPIView.as_view(),
        name='public_course_list',
    ),
    url(
        r'^courses/(?P<pk>[0-9a-z-]+)/$',
        PublicCourseDetailAPIView.as_view(),
        name='public_course_detail',
    ),
    url(
        r'^category/$',
        PublicCategoryCourseFullDetailApiView.as_view(),
        name='category_course_full_detail',
    ),
    url(
        r'^category/(?P<pk>[0-9a-z-]+)/$',
        PublicCategoryCourseDetailApiView.as_view(),
        name='category_course_detail',
    ),
]