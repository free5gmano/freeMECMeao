"""kube5gMEAO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.contrib import admin

from AppLifecycleManagement.views import *
from AppPackageManagement.views import *

Mm1_Mm3star_URI = {
    "ApplicationPackages": "app_pkgm/v1/app_packages",
    "ApplicationPackageContent": "app_pkgm/v1/app_packages/<str:app_package_Id>/package_content",
    "ApplicationInstances": "app_lcm/v1/app_instances",
    "InstantiateApplicationInstanceTask": "app_lcm/v1/app_instances/<str:appInstanceId>/instantiate",
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path(Mm1_Mm3star_URI["ApplicationPackages"], application_packages),
    path(Mm1_Mm3star_URI["ApplicationPackageContent"], application_package_content),
    path(Mm1_Mm3star_URI["ApplicationInstances"], application_instances),
    path(Mm1_Mm3star_URI["InstantiateApplicationInstanceTask"], instantiate_application_instance_task),
]