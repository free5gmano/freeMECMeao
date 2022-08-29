import io,os
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from VnfPackageManagement.serializers import *
from rest_framework import status
from django.utils.encoding import smart_str
from utils.file_manipulation import remove_file, decompress_zip, copy_file, compression_dir_zip,create_dir
# from utils.tosca_paser.base_package import disabled, enabled, not_in_use, created, on_boarded
from rest_framework.exceptions import APIException
from utils.tosca_paser.vnf_package import PackageVNF

class VNFPackagesViewSet(viewsets.ModelViewSet):
    
    
    queryset = VnfPkgInfo.objects.all()
    serializer_class = VnfPkgInfoSerializer
    def create(self, request, **kwargs):
        """
            Create a new individual VNF package resource.

            The POST method creates a new individual VNF package resource.
        """
        return super().create(request)
    def retrieve(self, request, *args, **kwargs):
        """
            Read information about an individual VNF package.

            The GET method reads the information of a VNF package.
        """
        return super().retrieve(request)

    def list(self, request, *args, **kwargs):
        """
            Query VNF packages information.

            The GET method queries the information of the VNF packages matching the filter. This method shall follow \
            the provisions specified in the Tables 9.4.2.3.2-1 and 9.4.2.3.2-2 for URI query parameters, request and \
            response data structures, and response codes.
        """
        return super().list(request)
    
    @action(detail=True, methods=['PUT', 'GET'], url_path='package_content')
    def upload_content(self, request, **kwargs):
        instance = self.get_object()
        if request.method == 'PUT':
            # if created != instance.onboardingState:
            #     raise APIException(detail='VNF Package onboardingState is not {}'.format(created),
            #                        code=status.HTTP_409_CONFLICT)
            if 'application/zip' not in request.META['HTTP_ACCEPT']:
                raise APIException(detail='HEAD need to have application/zip value')
            vnf_package_path = '{}{}'.format(vnf_package_base_path, instance.id)
            vnf_package_content_path = decompress_zip(
                request.data['file'], vnf_package_path + '/package_content/')
            process_vnf_instance = PackageVNF(path=vnf_package_content_path)
            
            input_value = process_vnf_instance.processing_data()
            serializer = self.get_serializer(instance, data=input_value)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(status=status.HTTP_202_ACCEPTED)
            