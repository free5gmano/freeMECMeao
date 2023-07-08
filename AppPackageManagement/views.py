import json
import uuid
import zipfile
import shutil
from django.http import JsonResponse
from AppPackageManagement.models import *
from django.http.multipartparser import MultiPartParser
from utils.zip_handler import *
from utils.tosca_parser import *
from utils.Mm1_Mm3star_Agent import *

def application_packages(request):
    result = {}
    status = 0
    if request.method == "POST":
        id_=uuid.uuid4()
        AppPkgInfo.objects.create(
            id=id_,
            appdId=None,
            appProvider=None,
            appProductName=None,
            appName=None,
            appSoftwareVersion=None,
            appdVersion=None,
            mecVersion=None,
            appInfoName=None,
            appDescription=None,
            swImageDescriptor=None,
            type=None,
            virtualComputeDescriptor="512Mi",
            virtualStorageDescriptor="250m",
            appExtCpd=None,
            appServiceRequired=None,
            appServiceOptional=None,
            appServiceProduced=None,
            appFeatureRequired=None,
            appFeatureOptional=None,
            transportDependencies=None,
            appTrafficRule=None,
            appDNSRule=None,
            appLatency="100ms",
            onboardingState="CREATED",
            operationalState="DISABLED",
            usageState="NOT_IN_USE",
            userDefinedData=None
        )
        result = {
            "id": id_,
            "appdId": None,
            "appProvider": None,
            "appProductName": None,
            "appName": None,
            "appSoftwareVersion": None,
            "appdVersion": None,
            "mecVersion": None,
            "appInfoName": None,
            "appDescription": None,
            "swImageDescriptor": None,
            "type": None,
            "virtualComputeDescriptor": "512Mi",
            "virtualStorageDescriptor": "250m",
            "appExtCpd": None,
            "appServiceRequired": None,
            "appServiceOptional": None,
            "appServiceProduced": None,
            "appFeatureRequired": None,
            "appFeatureOptional": None,
            "transportDependencies": None,
            "appTrafficRule": None,
            "appDNSRule": None,
            "appLatency": "100ms",
            "onboardingState": "CREATED",
            "operationalState": "DISABLED",
            "usageState": "NOT_IN_USE",
            "userDefinedData": None
        }
        status = 200
    else:
        pass
    return JsonResponse(result, status=status)    

def application_package_content(request, app_package_Id):
    result = {}
    status = 0
    if request.method == "PUT":
        #收檔案
        payload = MultiPartParser(request.META ,request, request.upload_handlers).parse()
        file_path_name = "./AppD/{file_name}".format(file_name=payload[1].get("file").name)
        
        handle_uploaded_file(file_path_name, payload[1].get("file"))
        #建資料夾
        app_package_path = "./AppD/{app_package_Id}".format(app_package_Id=app_package_Id)
        create_vnf_package_dir(app_package_path)
        #處理壓縮檔
        with zipfile.ZipFile(file_path_name, 'r') as zf:
            for name in zf.namelist():
                zf.extract(name, path=app_package_path+"/package_content/")
        
        vnfd_path = app_package_path+"/package_content/"+os.listdir(app_package_path+"/package_content/")[0]+"/Definitions/"
        vnfd_name = os.listdir(vnfd_path)[0]
        shutil.copyfile(vnfd_path+vnfd_name, app_package_path+"/appd/"+vnfd_name)
        #mapping vnfd nsd
        tosca = load_TOSCA(app_package_path+"/appd/"+vnfd_name)
        vnfd_pkg_path = generate_vnfd(app_package_Id, payload[1].get("file").name, tosca)
        #送NFVO
        
        nfvo_vnf_packages_result=nfvo_vnf_packages()
        nfvo_vnf_package_content(nfvo_vnf_packages_result["id"], vnfd_pkg_path.split("/").pop(), vnfd_pkg_path)
        nfvo_ns_descriptors_result=nfvo_ns_descriptors()
        nsdId = uuid.uuid4()
        generate_nsd(str(nsdId), tosca["node_types"]["properties"]["descriptor_id"]["default"], payload[1].get("file").name)
        nfvo_nsd_content(nfvo_ns_descriptors_result["id"])

        #存資料庫
        AppPkgInfo.objects.filter(id=app_package_Id).update(appdId=nfvo_vnf_packages_result["id"])
        NsInfo.objects.create(id=nsdId, app_package_Id=app_package_Id)

        os.remove(file_path_name)

        result = {"id": nsdId}
        status = 202
    else:
        pass
    return JsonResponse(result, status=status, safe=False)    

