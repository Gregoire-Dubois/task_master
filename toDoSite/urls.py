"""toDoSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import include, path, re_path
from dj_rest_auth.registration.views import VerifyEmailView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView, UserDetailsView

from dj_rest_auth.registration.views import VerifyEmailView

from django.views.generic import TemplateView

schema_view = get_schema_view(
   openapi.Info(
      title="To Do API",
      default_version='v1',
      description="This API is for use to 'do application'",
      #terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="gregoire.dominiquedubois@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('', include('toDo_app.urls')),
    path('api-auth/', include('rest_framework.urls')),

    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),


    path('dj-rest-auth/password/reset/', PasswordResetView.as_view(), name='reset_password'),
    path('dj-rest-auth/password/reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),

    path('dj-rest-auth/password/change/', PasswordChangeView.as_view(), name='change_password'),

    path('/dj-rest-auth/user/', UserDetailsView.as_view(), name='user_detail')

    #a faire : path('/dj-rest-auth/token/verify/',)

]
