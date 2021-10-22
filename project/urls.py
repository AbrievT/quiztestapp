"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.documentation import include_docs_urls

from project.drf_yasg import yasg_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', yasg_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', include_docs_urls(title='Quiz app', description='A web api of Quiz app models ')),
    path('v1/', include('apps.quiz.urls')),
]
