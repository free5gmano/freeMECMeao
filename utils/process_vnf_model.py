import os
import json
import random
import string
from NSInstanceManagement.models import VnfInstance
from VnfPackageManagement.models import VnfPkgInfo
from utils.file_manipulation import read_yaml_file,load_yaml_file

vnf_package_base_path = os.getcwd() + "/VnfPackage/"
def get_vnf_instance(vnf_pkg_ids) -> list:
    vnf_instances = list()
    for vnf_pkg_id in vnf_pkg_ids:
        # mec_app_path=get_root_path(vnf_pkg_id)
        # tosca_metadata = read_yaml_file('{}TOSCA-Metadata/TOSCA.meta'.format(mec_app_path))
        # entry_definitions = tosca_metadata['Entry-Definitions']
        # print(mec_app_path + entry_definitions)
        # mec_data=(load_yaml_file(mec_app_path + entry_definitions))
        # print(mec_data)
        vnf_package_info = VnfPkgInfo.objects.filter(id=vnf_pkg_id).last()
        vnfd_id = vnf_package_info.appdId.lower()
        vnf_instance_name = '{}-{}'.format(vnfd_id, randomString())
        print(vnf_package_info.appName)
        print(vnf_package_info.appInfoName)
        vnf_instances.append({'vnfdId': vnfd_id,
                              'vnfInstanceName': vnf_instance_name,
                              'vnfProvider': vnf_package_info.appProvider,
                              'vnfProductName': vnf_package_info.appProductName,
                              'vnfSoftwareVersion': vnf_package_info.appSoftwareVersion,
                              'vnfdVersion': vnf_package_info.mecVersion,
                              'vnfPkgId': vnf_pkg_id,
                              'metadata': vnf_package_info.userDefinedData,
                              'appName':vnf_package_info.appName,
                              'appInfoName':vnf_package_info.appInfoName,
                              'instantiationState': 'STARTED'})
    return vnf_instances
def get_platform_service_data(vnf_pkg_id):
    vnf_package_info = VnfPkgInfo.objects.filter(id=vnf_pkg_id).last()
    platform_service_data=dict()
    platform_service_data["platform_type"]=vnf_package_info.appServiceRequired
    platform_service_data["platform_describe"]=vnf_package_info.appFeatureRequired
    return platform_service_data

def get_root_path(package_id):
    root, dirs, files = walk_file('{}{}'.format(vnf_package_base_path, package_id), 'package_content')
    return '{}/{}/'.format(root, dirs.pop(0)) 

def walk_file(path, key):
    for root, dirs, files in os.walk(path):
        if key in root:
            return root, dirs, files
        
def randomString(stringLength=5):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, stringLength))