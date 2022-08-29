from django.urls import path, include
from rest_framework.routers import DefaultRouter
from NSInstanceManagement import views

router = DefaultRouter()
router.register(r'ns_instances', views.NSInstanceViewSet)

urlpatterns = [
    path('mec_nslcm/v1/', include(router.urls)),
]
