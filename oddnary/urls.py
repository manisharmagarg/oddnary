"""oddnary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
# jwt import
from rest_framework_simplejwt import views as jwt_views
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls,
    ),
    url(
        r'^api/account/', 
        include('account.urls'),
    ),
    # url(
    #     r'^api/token/$',
    #     jwt_views.TokenObtainPairView.as_view(),
    #     name='token_obtain_pair',
    # ),
    # url(
    #     r'^api/token/refresh/$',
    #     jwt_views.TokenRefreshView.as_view(),
    #     name='token_refresh',
    # ),
    url(
        r'^api/docs/',
        include_docs_urls(title='Oddnary',),
    ),
    url(
        r'^api/courses/',
        include('courses.urls'),
    ),
    url(
        r'^api/assignments/',
        include('assignments.urls'),
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)