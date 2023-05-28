import os

from rest_framework import serializers
from VnfPackageManagement.models import *
from utils.file_manipulation import remove_file, decompress_zip, copy_file, compression_dir_zip,create_dir

vnf_package_base_path = os.getcwd() + "/VnfPackage/"
create_dir(vnf_package_base_path)
class VnfPkgInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VnfPkgInfo
        fields = '__all__'

    def create(self, validated_data):
        vnf_package_info = VnfPkgInfo.objects.create(**validated_data)
        return vnf_package_info