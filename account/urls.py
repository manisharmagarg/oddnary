from django.conf.urls import url

from .views import (
    SignUpView,
    SubscriberLoginAPIView,
    InstructorLoginAPIView,
    AdminLoginAPIView,
    RefreshTokenAPIView,
    UserDetailApiView,
    UserListApiView,
    PasswordResetApiView,
)

app_name = 'account'

urlpatterns = [
    url(
        r'^signup/$',
        SignUpView.as_view(),
        name='signup',
    ),
    url(
        r'^subscriber/login/$',
        SubscriberLoginAPIView.as_view(),
        name='admin-login',
    ),
    url(
        r'^instructor/login/$',
        InstructorLoginAPIView.as_view(),
        name='admin-login',
    ),
    url(
        r'^admin/login/$',
        AdminLoginAPIView.as_view(),
        name='admin-login',
    ),
    url(
        r'^token/refresh/$',
        RefreshTokenAPIView.as_view(),
        name='admin-login',
    ),
    url(
        r'^user/$',
        UserDetailApiView.as_view(),
        name='user-detail',
    ),
    url(
        r'^admin/users/$',
        UserListApiView.as_view(),
        name='users-list',
    ),
    url(
        r'^change-password/$',
        PasswordResetApiView.as_view(),
        name='change-password',
    ),
]


