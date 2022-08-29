import uuid
from django.db import models

# Create your models here.

class NsInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nsInstanceName = models.TextField()
    nsInstanceDescription = models.TextField()
    nsdId = models.TextField()
    nsdInfoId = models.TextField()
    platformName = models.TextField(null=True, blank=True)
    deployedCluster = models.TextField(null=True, blank=True)
    nestedNsInstanceId = models.TextField(null=True, blank=True)
    flavourId = models.TextField(null=True, blank=True)
    nestedNsInstanceId = models.TextField(null=True, blank=True)
    nsState = models.TextField(default='NOT_INSTANTIATED')
    
class VnfInstance(models.Model):
    vnfInstance = models.ForeignKey(NsInstance,
                                    null=True,
                                    blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='NsInstance_VnfInstance')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vnfInstanceName = models.TextField(null=True, blank=True)
    vnfInstanceDescription = models.TextField(null=True, blank=True)
    vnfdId = models.TextField()
    vnfProvider = models.TextField()
    vnfProductName = models.TextField()
    vnfSoftwareVersion = models.TextField()
    vnfdVersion = models.TextField()
    vnfPkgId = models.TextField()
    appName= models.TextField()
    appInfoName= models.TextField()
    vnfConfigurableProperties = models.TextField(null=True, blank=True)
    vimId = models.TextField(null=True, blank=True)
    instantiationState = models.TextField(default='NOT_INSTANTIATED')
    metadata = models.TextField(null=True, blank=True)
    extensions = models.TextField(null=True, blank=True)

