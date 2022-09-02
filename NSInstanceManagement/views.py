from email import utils
import os
import json
from django.shortcuts import render
from NSInstanceManagement.serializers import *
from NSManagement.serializers import *
from VnfPackageManagement.serializers import *
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework import viewsets
from utils.process_vnf_model import get_vnf_instance,get_platform_service_data
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.mv1_module.mv1_agent import Mv1Agent

# Create your views here.
instantiated_state = (instantiated, not_instantiated) = ('INSTANTIATED', 'NOT_INSTANTIATED')
class NSInstanceViewSet(viewsets.ModelViewSet):
    queryset = NsInstance.objects.all()
    serializer_class = NsInstanceSerializer

    def create(self, request, *args, **kwargs):
        """
            Create a new NS descriptor resource.

            The POST method is used to create a new NS descriptor resource.
        """
        
        if 'nsdId' not in request.data:
            raise APIException(detail='nsdId is not existing',
                               code=status.HTTP_409_CONFLICT)

        if 'nsName' not in request.data:
            raise APIException(detail='nsName is not existing',
                               code=status.HTTP_409_CONFLICT)

        if 'nsDescription' not in request.data:
            raise APIException(detail='nsDescription is not existing',
                               code=status.HTTP_409_CONFLICT)
        ns_descriptors_info = NsdInfo.objects.filter(nsdId=request.data['nsdId']).last()
        if ns_descriptors_info is None:
            raise APIException(detail='nsdId is not existing',
                               code=status.HTTP_409_CONFLICT)
        vnf_pkg_Ids = json.loads(ns_descriptors_info.appPkgIds)
        nsd_info_id = str(ns_descriptors_info.id)
        request.data['nsdInfoId'] = nsd_info_id
       
        request.data['nsInstanceName'] = request.data['nsName']
        request.data['nsInstanceDescription'] = request.data['nsDescription']
        request.data['nsdId'] = request.data['nsdId']
        request.data['deployedCluster'] = ns_descriptors_info.deployedCluster
        request.data['platformName'] = ns_descriptors_info.platformName
        request.data['vnfInstance'] = get_vnf_instance(vnf_pkg_Ids)
        return super().create(request)

    def list(self, request, *args, **kwargs):
        """
            Query information about multiple NS descriptor resources.

            The GET method queries information about multiple NS descriptor resources.
        """
        if self.get_queryset().__len__() < 1:
            raise APIException(detail='One or more individual NS descriptor resource have been created')

        return super().list(request)

    def retrieve(self, request, *args, **kwargs):
        """
            Read information about an individual NS descriptor resource.

            The GET method reads information about an individual NS descriptor.
        """
        return super().retrieve(request)
    
    @action(detail=True, methods=['POST'], url_path='instantiate')
    def instantiate_ns(self, request, **kwargs):
        """
            Instantiate a NS.
            The POST method requests to instantiate a NS instance resource.
        """
        ns_instance = self.get_object()

        if 'vnfInstanceData' not in request.data:
            raise APIException(detail='vnfInstanceData is not existing',
                               code=status.HTTP_409_CONFLICT)
            
        vnf_instance_list = list()
        ns_type="platform"
        helm_chart=dict()
        
        mv1=Mv1Agent(cluster_name=ns_instance.deployedCluster,mec_platform_name=ns_instance.platformName)
        vnf_instance_data = request.data.pop('vnfInstanceData')
        if ns_instance.platformName != "None":
            check_mec=mv1.checkMEC()
            if check_mec.json()["status"] == "succeed":
                ns_type="app"
            else :
                return Response("MEC Platform not exist",status=status.HTTP_202_ACCEPTED)
    
        for vnf_instance_info in vnf_instance_data:
            if 'vnfInstanceId' not in vnf_instance_info:
                raise APIException(detail='vnfInstanceId is not existing',
                                   code=status.HTTP_409_CONFLICT)
            vnf_instance = ns_instance.NsInstance_VnfInstance.get(id=vnf_instance_info['vnfInstanceId'])
            if vnf_instance is None:
                raise APIException(detail='vnf_instance is not existing',
                                   code=status.HTTP_409_CONFLICT)
            if ns_type == "app":
                if vnf_instance.vnfProductName in helm_chart:
                    print("helm chart exist")
                else:
                    helm_chart[vnf_instance.vnfProductName]=vnf_instance.vnfProvider
                    mv1.addHelmChart(repoName=vnf_instance.vnfProductName,repoUrl=vnf_instance.vnfProvider)
                platform_service_data=get_platform_service_data(vnf_instance.vnfPkgId)
                mv1.createMECApp(repoName=vnf_instance.vnfProductName,mecApp=vnf_instance.appInfoName,mecName=vnf_instance.appName,
                                serviceType=platform_service_data['platform_type'],service=platform_service_data['platform_describe'])
            else :
                platform_check=mv1.checkMEC()
                print(platform_check.json()["status"])
                if platform_check.json()["status"] == "succeed":
                    print("platform exist" )
                else:
                    print("create Platform")
                    mv1.createMEC()
            vnf_instance.instantiationState = 'STARTED'
            vnf_instance.save()

        ns_instance.nsState = instantiated
        ns_instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    @action(detail=True, methods=['POST'], url_path='terminate')
    def terminate_ns(self, request, **kwargs):
        ns_instance = self.get_object()
        if 'vnfInstanceData' not in request.data:
            raise APIException(detail='vnfInstanceData is not existing',
                               code=status.HTTP_409_CONFLICT)
        vnf_instance_data = request.data.pop('vnfInstanceData')
        mv1=Mv1Agent(cluster_name=ns_instance.deployedCluster,mec_platform_name=ns_instance.platformName)
        ns_type="platform"
        if ns_instance.platformName != "None":
            ns_type="app"
        for vnf_instance_info in vnf_instance_data:
            if 'vnfInstanceId' not in vnf_instance_info:
                raise APIException(detail='vnfInstanceId is not existing',
                                   code=status.HTTP_409_CONFLICT)
            vnf_instance = ns_instance.NsInstance_VnfInstance.get(id=vnf_instance_info['vnfInstanceId'])
            if ns_type=="app":
                platform_service_data=get_platform_service_data(vnf_instance.vnfPkgId)
                mv1.deleteMECApp(serviceType=platform_service_data['platform_type'],service=platform_service_data['platform_describe'])
            else:
                mv1.deleteMECPlatform()
                vnf_instance.VnfInstance_instantiatedVnfInfo.vnfState = 'STOPPED'
                vnf_instance.VnfInstance_instantiatedVnfInfo.save()
        ns_instance.nsState = instantiated
        ns_instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)