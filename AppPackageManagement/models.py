import uuid
from django.db import models

# Create your models here.

class AppPkgInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appdId = models.TextField(null=True, blank=True)
    appProvider = models.TextField(null=True, blank=True)
    appProductName = models.TextField(null=True, blank=True)
    appName = models.TextField(null=True, blank=True)
    appSoftwareVersion = models.TextField(null=True, blank=True)
    appdVersion = models.TextField(null=True, blank=True)
    mecVersion = models.TextField(null=True, blank=True)
    appInfoName = models.TextField(null=True, blank=True)
    appDescription = models.TextField(null=True, blank=True)
    swImageDescriptor = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    virtualComputeDescriptor = models.TextField(default="512Mi")
    virtualStorageDescriptor = models.TextField(default="250m")
    appExtCpd = models.TextField(null=True, blank=True)
    appServiceRequired = models.TextField(null=True, blank=True)
    appServiceOptional = models.TextField(null=True, blank=True)
    appServiceProduced = models.TextField(null=True, blank=True)
    appFeatureRequired = models.TextField(null=True, blank=True)
    appFeatureOptional = models.TextField(null=True, blank=True)
    transportDependencies = models.TextField(null=True, blank=True)
    appTrafficRule = models.TextField(null=True, blank=True)
    appDNSRule = models.TextField(null=True, blank=True)
    appLatency = models.TextField(default="100ms")
    onboardingState = models.TextField(default="CREATED")
    operationalState = models.TextField(default="DISABLED")
    usageState = models.TextField(default="NOT_IN_USE")
    userDefinedData = models.TextField(null=True, blank=True)
    
class NsInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_package_Id = models.TextField(null=True, blank=True)
