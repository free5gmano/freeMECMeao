import requests
import json
import os
import yaml
import zipfile
import shutil
from kube5gMEAO.settings import NFVO_PATH

def nfvo_vnf_packages():
    url = "http://" + NFVO_PATH + "/vnfpkgm/v1/vnf_packages/"
    payload={}
    response = requests.request("POST", url, data=payload)
    return json.loads(response.text)

def nfvo_vnf_package_content(vnf_package_Id, file_name, path):
    url = "http://" + NFVO_PATH + "/vnfpkgm/v1/vnf_packages/" + vnf_package_Id + "/package_content/"
    payload={}
    files=[
    ('file',(file_name, open(path,'rb'),'application/zip'))
    ]
    headers = {
    'Accept': 'application/zip, application/json',
    }
    response = requests.request("PUT", url, headers=headers, data=payload, files=files)

def nfvo_ns_descriptors():
    url = "http://" + NFVO_PATH + "/nsd/v1/ns_descriptors/"
    payload={}
    response = requests.request("POST", url, data=payload)
    return json.loads(response.text)
    
def generate_nsd(nsd_id ,vnfd_id, file_name):
    try:
        os.mkdir("NSD/ns")
    except Exception as e:
        pass
    try:
        os.mkdir("NSD/ns/ns")
    except Exception as e:
        pass
    try:
        os.mkdir("NSD/ns/ns/Definitions")
    except Exception as e:
        pass
    try:
        os.mkdir("NSD/ns/ns/Files")
    except Exception as e:
        pass
    try:
        os.mkdir("NSD/ns/ns/TOSCA-Metadata")
    except Exception as e:
        pass
    ns_yaml={
        "tosca_definitions_version": "tosca_simple_yaml_1_2",
        "topology_template": {
            "node_templates": {
                "NS1": {
                    "type": "tosca.nodes.nfv.NS",
                    "properties":{
                        "descriptor_id": nsd_id,
                        "designer": "imac",
                        "version": 1.0,
                        "name": "free5gc-stage3.2.1",
                        "invariant_id": "1111-2222-aaaa-bbbb",
                        "constituent_vnfd":[
                            {
                                "vnfd_id": vnfd_id
                            }
                        ]
                    }   
                }
            } 
        }
    }
    with open('NSD/ns/ns/Definitions/ns.yaml', 'w') as file:
        documents = yaml.dump(ns_yaml, file)

    with open('NSD/ns/ns/Files/ChangeLog.txt', 'w') as file:
        pass

    tosca_mata={
        "TOSCA-Meta-File-Version": 1.0,
        "CSAR-Version": 1.1,
        "Created-By": "imac",
        "Entry-Definitions": "Definitions/ns.yaml",
        "ETSI-Entry-Manifest": file_name.split(".")[0]+".mf",
        "ETSI-Entry-Change-Log": "Files/ChangeLog.txt",
        "ETSI-Entry-Licenses": "Files/Licenses"
    }

    with open('NSD/ns/ns/TOSCA-Metadata/TOSCA.meta', 'w') as file:
        documents = yaml.dump(tosca_mata, file)

    mf={
        "metadata": {
            "vnf_product_name": file_name.split(".")[0],
            "vnf_provider_id": "imac",
            "vnf_package_version": 1.2,
            "vnf_release_date_time": "2022-01-20T11:20:43+03:00"
        }
    }

    with open('NSD/ns/ns/'+file_name.split(".")[0]+".mf", 'w') as file:
        documents = yaml.dump(mf, file)

    shutil.make_archive("./NSD/ns", 'zip', './NSD/ns')

def nfvo_nsd_content(nsd_Id):
    url = "http://" + NFVO_PATH + "/nsd/v1/ns_descriptors/"+ nsd_Id +"/nsd_content/"

    payload={}
    files=[
    ('file',('ns.zip',open('NSD/ns.zip','rb'),'application/zip'))
    ]
    headers = {
    'Accept': 'application/zip, application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, files=files)

def nfvo_ns_instances(nsd_Id):
    url = "http://" + NFVO_PATH + "/nslcm/v1/ns_instances/"

    payload = json.dumps({
        "nsdId": str(nsd_Id),
        "nsName": "String",
        "nsDescription": "String"
    })
    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


def nfvo_instantiate(nfvo_ns_instances_result):
    url = "http://" + NFVO_PATH + "/nslcm/v1/ns_instances/" + nfvo_ns_instances_result["id"] + "/instantiate/"
    
    payload = {"vnfInstanceData": []}
    
    for vnfInstance in nfvo_ns_instances_result["vnfInstance"]:
        payload["vnfInstanceData"].append({
            "vnfInstanceId": vnfInstance["id"],
            "vnfProflieId": "String",
        })
    
    payload = json.dumps(payload)

    headers = {
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)




