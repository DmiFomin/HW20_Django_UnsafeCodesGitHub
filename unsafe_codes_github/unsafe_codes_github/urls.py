"""unsafe_codes_github URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers
from searching_unsafe_codes.views_api import SettingsViewSet, StatusesViewSet, LanguagesViewSet, UnsafeCodesViewSet
from users_and_permissions.views_api import AdvancedUserViewSet


router = routers.DefaultRouter()
router.register(r'users', AdvancedUserViewSet)
router.register(r'settings', SettingsViewSet)
router.register(r'statuses', StatusesViewSet)
router.register(r'languages', LanguagesViewSet)
router.register(r'languages', LanguagesViewSet)
router.register(r'unsafe_codes', UnsafeCodesViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('searching_unsafe_codes.urls', namespace='searching_unsafe_codes')),
    path('users/', include('users_and_permissions.urls', namespace='users_and_permissions')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/0/', include(router.urls)),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns