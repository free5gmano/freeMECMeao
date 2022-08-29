from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.utils import json

from NSManagement.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from VnfPackageManagement.models import *
from utils.file_manipulation import  decompress_zip
from utils.tosca_paser.ns_package import PackageNS


class NSManagementViewSet(viewsets.ModelViewSet):
    queryset = NsdInfo.objects.all()
    serializer_class = NsdInfoSerializer
    def create(self, request, *args, **kwargs):
        """
            Create a new NS descriptor resource.

            The POST method is used to create a new NS descriptor resource.
        """
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


    @action(detail=True, methods=['PUT', 'GET'], url_path='nsd_content')
    def upload_content(self, request, **kwargs):
        instance = self.get_object()
        if request.method == 'PUT':
            if 'application/zip' not in request.META['HTTP_ACCEPT']:
                raise APIException(detail='HEAD need to have application/zip value')

            network_service_path = decompress_zip(
                request.data["file"], '{}{}'.format(nsd_base_path, instance.id) + '/nsd_content/')
            network_service_descriptor = PackageNS(path=network_service_path)
            nsd_content = network_service_descriptor.processing_data()
           
            vnfPkgIds_list = list()
            
            for appd in network_service_descriptor.get_constituent_vnfd():
                vnfPkgIds_list.append(str(VnfPkgInfo.objects.filter(appdId__iexact=appd['appd_id']).last().id))
            nsd_content['appPkgIds'] = json.dumps(vnfPkgIds_list)
            print(nsd_content)
            serializer = self.get_serializer(instance, data=nsd_content)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
