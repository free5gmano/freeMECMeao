import os
import uuid

def handle_uploaded_file(file_name, files):
    with open(file_name, 'wb+') as destination:
        for chunk in files.chunks():
            destination.write(chunk)

def create_vnf_package_dir(vnf_package_id):
    try:
        os.mkdir(vnf_package_id)
    except Exception as e:
        pass
    try:
        os.mkdir(vnf_package_id+"/package_content")
    except Exception as e:
        pass
    try:
        os.mkdir(vnf_package_id+"/appd")
    except Exception as e:
        pass

def create_ns_descriptors_dir(ns_descriptors_id):
    try:
        os.mkdir(ns_descriptors_id)
    except Exception as e:
        pass
    try:
        os.mkdir(ns_descriptors_id+"/nsd_content")
    except Exception as e:
        pass