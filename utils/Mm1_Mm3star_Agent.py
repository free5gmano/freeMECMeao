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
        documents = yaml.dump(ns_yaml, file, sort_keys=False)

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

def generate_vnfd(vnfd_id, file_name, tosca):
    try:
        os.mkdir("VNFD/vnf")
    except Exception as e:
        pass
    try:
        os.mkdir("VNFD/vnf/"+vnfd_id+"/")
    except Exception as e:
        pass
    try:
        os.mkdir("VNFD/vnf/"+vnfd_id+"/"+vnfd_id)
    except Exception as e:
        pass
    try:
        os.mkdir("VNFD/vnf/"+vnfd_id+"/"+vnfd_id+"/Definitions")
    except Exception as e:
        pass
    try:
        os.mkdir("VNFD/vnf/"+vnfd_id+"/"+vnfd_id+"/Files")
    except Exception as e:
        pass
    try:
        os.mkdir("VNFD/vnf/"+vnfd_id+"/"+vnfd_id+"/TOSCA-Metadata")
    except Exception as e:
        pass
    vnf_yaml={
        "tosca_definitions_version": tosca["tosca_definitions_version"],
        "topology_template": {
            "node_templates": {
                "VNF1": {
                    "type": "tosca.nodes.nfv.VNF",
                    "properties":{
                        "descriptor_id": tosca["node_types"]["properties"]["descriptor_id"]["default"],
                        "descriptor_version": tosca["node_types"]["properties"]["descriptor_version"]["default"],
                        # "provider": tosca["node_types"]["properties"]["provider"]["default"],
                        "provider": "chsixnine",
                        "product_name": tosca["node_types"]["properties"]["product_name"]["default"],
                        "software_version": tosca["node_types"]["properties"]["software_version"]["default"],
                    }   
                },
                "VDU1": {
                    "type": "tosca.nodes.nfv.Vdu.Compute",
                    "properties":{
                        "sw_image_data": {
                            # "name": tosca["topology template"]["node_templates"]["MyMecAppStorage"]["artifacts"]["sw_image"]["properties"]["name"],
                            "name": "statful-test",
                            # "provider": tosca["node_types"]["properties"]["provider"]["default"],
                            "provider": "chsixnine",
                            "version": tosca["topology template"]["node_templates"]["MyMecAppStorage"]["artifacts"]["sw_image"]["properties"]["version"],
                            "diskFormat": "raw"
                        }
                    },
                    "capabilities": {
                        "virtual_compute":{
                            "properties":{
                                "virtual_memory":{
                                    # "virtual_mem_size": tosca["topology template"]["node_templates"]["MyMecAppNode"]["capabilities"]["virtual_compute"]["properties"]["virtual_memory"]["virtual_mem_size"]
                                    "virtual_mem_size": "512Mi"
                                },
                                "virtual_cpu":{
                                    "num_virtual_cpu": tosca["topology template"]["node_templates"]["MyMecAppNode"]["capabilities"]["virtual_compute"]["properties"]["virtual_cpu"]["num_virtual_cpu"]
                                }
                            }
                        }
                    },
                    "artifacts":{
                        "sw_image":{
                            "type": "tosca.artifacts.nfv.SwImage",
                            # "file": tosca["topology template"]["node_templates"]["MyMecAppStorage"]["artifacts"]["sw_image"]["file"]
                            "file": "chsixnine/statful-test:1.0.5"
                        }
                    },
                    "attributes":{
                        "namespace": "default",
                        "replicas": 1,
                        "name_of_service": "statful-test-svc",
                        "ports":[25000]
                    }
                },
                "CP1": {
                    "type": "tosca.nodes.nfv.Cpd",
                    "properties": {
                        "layer_protocol": "ipv4"
                    },
                    "requirements": {
                        "virtual_binding": "VDU1",
                        "virtual_link": "VL1"
                    }
                },
                "VL1": {
                    "type": "tosca.nodes.nfv.VnfVirtualLink",
                    "properties": {
                        "network_name": "management",
                        "vl_profile": {
                            "virtual_link_protocol_data": {
                                "l3_protocol_data": {
                                    "dhcp_enabled": False
                                }
                            }
                        }
                    }
                        
                }
            } 
        }
    }

    input(vnf_yaml)

    with open('VNFD/vnf/'+vnfd_id+"/"+vnfd_id+'/Definitions/'+vnfd_id+'.yaml', 'w') as file:
        documents = yaml.dump(vnf_yaml, file, sort_keys=False)

    with open('VNFD/vnf/'+vnfd_id+"/"+vnfd_id+'/Files/ChangeLog.txt', 'w') as file:
        pass

    tosca_mata={
        "TOSCA-Meta-File-Version": 1.0,
        "CSAR-Version": 1.1,
        "Created-By": "imac",
        "Entry-Definitions": "Definitions/"+vnfd_id+".yaml",
        "ETSI-Entry-Manifest": file_name.split(".")[0]+".mf",
        "ETSI-Entry-Change-Log": "Files/ChangeLog.txt",
        "ETSI-Entry-Licenses": "Files/Licenses"
    }

    with open('VNFD/vnf/'+vnfd_id+"/"+vnfd_id+'/TOSCA-Metadata/TOSCA.meta', 'w') as file:
        documents = yaml.dump(tosca_mata, file)

    mf={
        "metadata": {
            "vnf_product_name": file_name.split(".")[0],
            "vnf_provider_id": "imac",
            "vnf_package_version": 1.2,
            "vnf_release_date_time": "2022-01-20T11:20:43+03:00"
        }
    }

    with open('VNFD/vnf/'+vnfd_id+"/"+vnfd_id+'/'+file_name.split(".")[0]+".mf", 'w') as file:
        documents = yaml.dump(mf, file)

    shutil.make_archive("./VNFD/vnf/"+vnfd_id+"/", 'zip', './VNFD/vnf/'+vnfd_id+"/")

    return "./VNFD/vnf/"+vnfd_id+".zip"


