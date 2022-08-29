from django.urls import path, include
from rest_framework.routers import DefaultRouter
from NSManagement import views

router = DefaultRouter()
router.register(r'ns_descriptors', views.NSManagementViewSet)

urlpatterns = [
    path('mec_nsd/v1/', include(router.urls)),
]
