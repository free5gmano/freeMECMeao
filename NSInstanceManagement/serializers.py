import os
import json

from rest_framework import serializers
from utils.file_manipulation import create_dir
from .models import *

class VnfInstanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VnfInstance
        fields = ('id', 'vnfInstanceName', 'vnfdId', 'vnfProvider', 'vnfProductName', 'vnfdVersion',
                  'vnfPkgId', 'instantiationState','vnfSoftwareVersion','appName','appInfoName')
        
class NsInstanceSerializer(serializers.ModelSerializer):
    vnfInstance = VnfInstanceSerializer(many=True, required=False, source='NsInstance_VnfInstance')

    class Meta:
        model = NsInstance
        fields = '__all__'

    def create(self, validated_data):
        vnf_Instance_dict = validated_data.pop('NsInstance_VnfInstance', dict())
        ns = NsInstance.objects.create(**validated_data)
        for vnf_Instance_value in vnf_Instance_dict:
            vnf_Instance = VnfInstance.objects.create(**vnf_Instance_value)
            ns.NsInstance_VnfInstance.add(vnf_Instance)
        return ns
    

