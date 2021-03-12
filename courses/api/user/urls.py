# Django imports
from django.conf.urls import url, include

# Local imports
from .views import (
    UserCourseListAPIView,
    UserCourseDetailAPIView,
    AddCourseInMyCoursesAPIView,
    DeleteCourseFromMyCoursesAPIView,
    UserCategoryCourseFullDetailApiView,
    UserCategoryCourseDetailApiView,
)

urlpatterns = [
    url(
        r'^courses/$',
        UserCourseListAPIView.as_view(),
        name='user_course_list',
    ),
    url(
        r'^course/(?P<pk>[0-9a-z-]+)/$',
        UserCourseDetailAPIView.as_view(),
        name='user_course_detail',
    ),
    url(
        r'^add-course/$',
        AddCourseInMyCoursesAPIView.as_view(),
        name='user_add_course',
    ),
    url(
        r'^remove-course/(?P<pk>[0-9a-z-]+)/$',
        DeleteCourseFromMyCoursesAPIView.as_view(),
        name='user_remove_course',
    ),
    url(
        r'^category/$',
        UserCategoryCourseFullDetailApiView.as_view(),
        name='category_course_full_detail',
    ),
    url(
        r'^category/(?P<pk>[0-9a-z-]+)/$',
        UserCategoryCourseDetailApiView.as_view(),
        name='category_course_detail',
    ),
]