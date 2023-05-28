# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from CloudEdgeClusterManager import views
#
# router = DefaultRouter()
# router.register(r'manage', views.CloudEdgeClusterManagerViewSet, basename='clustermanager')
#
# urlpatterns = [
#     path('clustermanager', include(router.urls)),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from VnfPackageManagement import views

router = DefaultRouter()
router.register(r'app_packages', views.VNFPackagesViewSet)

urlpatterns = [
    path('app_pkgm/v1/', include(router.urls)),
]
