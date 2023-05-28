from django.http import JsonResponse
from utils.tosca_parser import *
from utils.Mm1_Mm3star_Agent import *
from VnfPackageManagement.models import *
from AppLifecycleManagement.models import *
import uuid

# Create your views here.
def application_instances(request):
    result = {}
    status = 0
    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))
        vnf_pkg_info=VnfPkgInfo.objects.filter(appdId=payload["nsdId"])
        # print(vnf_pkg_info["id"])
        app_instance_id = uuid.uuid4()
        AppInstanceInfo.objects.create(id=app_instance_id, appdId=payload["nsdId"])
        result = {
            "id": app_instance_id,
            "vnfInstance": [
                {
                "id": "11660d54-3c3a-4c0d-b70e-7cf8983d4f0d",
                "vnfInstanceName": "367f45fd-1dd2-11b2-8001-080027ubuntu-yxjvk",
                "vnfdId": "hbhb",
                "vnfProvider": "free5gmano",
                "vnfProductName": "free5gmano",
                "vnfdVersion": "laster",
                "vnfPkgId": "8f7bc531-d6e1-4185-b1fe-375129ab5096",
                "instantiationState": "STARTED",
                "vnfSoftwareVersion": "latest",
                "appName": "ubuntu",
                "appInfoName": "ubuntu"
                }
            ],
            "nsInstanceName": "String",
            "nsInstanceDescription": "String",
            "nsdId": "1b4dd4c7-1dd2-11b2-8000-080027b246c9",
            "nsdInfoId": "58e77cf3-ecff-4890-b371-1596bb5914cf",
            "platformName": "None",
            "deployedCluster": "edge",
            "flavourId": None,
            "nestedNsInstanceId": None,
            "nsState": "NOT_INSTANTIATED"
        }
        status = 201
    else:
        pass
    return JsonResponse(result, status=status, safe=False)

def instantiate_application_instance_task(request, appInstanceId):
    result = {}
    status = 0
    if request.method == "POST":
        payload = json.loads(request.body.decode("utf-8"))

        app_instance_info=AppInstanceInfo.objects.get(id=appInstanceId)
        print(app_instance_info.appdId)
        vnf_pkg_info=VnfPkgInfo.objects.get(appdId=app_instance_info.appdId)
        ns_info = NsInfo.objects.get(app_package_Id=vnf_pkg_info.id)

        nfvo_ns_instances_result = nfvo_ns_instances(ns_info.id)
        nfvo_instantiate(nfvo_ns_instances_result)

        result = 1
        status = 202
    else:
        pass
    return JsonResponse(result, status=status, safe=False)