from django.db import models
import uuid

class NsdInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nsdId = models.TextField(null=True, blank=True)
    nsdName = models.TextField(null=True, blank=True)
    nsdVersion = models.TextField(null=True, blank=True)
    nsdDesigner = models.TextField(null=True, blank=True)
    platformName = models.TextField(null=True, blank=True)
    nsdInvariantId = models.TextField(null=True, blank=True)
    deployedCluster = models.TextField(null=True, blank=True)
    appPkgIds = models.TextField(null=True, blank=True)
    pnfdInfoIds = models.TextField(null=True, blank=True)
    nestedNsdInfoIds = models.TextField(null=True, blank=True)
    nsdOnboardingState = models.TextField(default="CREATED")
    nsdOperationalState = models.TextField(default="DISABLED")
    nsdUsageState = models.TextField(default="NOT_IN_USE")
    userDefinedData = models.TextField(null=True, blank=True)