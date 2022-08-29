from utils.file_manipulation import sha256_hash
import yaml
from utils.file_manipulation import read_yaml_file,load_yaml_file
class PackageVNF():

    def __init__(self, path=None):
        self.tosca_metadata = read_yaml_file('{}TOSCA-Metadata/TOSCA.meta'.format(path))
        self.entry_definitions = self.tosca_metadata['Entry-Definitions']
        self.mec_data=(load_yaml_file(path + self.entry_definitions))
    def processing_data(self):
        result = dict()
        if self.mec_data['topology_template']['node_templates']['VNF']["type"] == "tosca.nodes.nfv.platform":
            result = {'appdId': self.mec_data['topology_template']['node_templates']['VNF']["properties"]['descriptor_id'],
                    'appProvider': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['provider'],
                    'appProductName': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['provider_name'],
                    'type': 'platform',
                    'appName': self.mec_data['topology_template']['node_templates']['VNF']["properties"]['product_name'],
                    'appSoftwareVersion': self.mec_data['topology_template']['node_templates']['VNF']["properties"]['software_version'],
                    'appdVersion': self.mec_data['topology_template']['node_templates']['VNF']["properties"]['descriptor_version'],
                    'mecVersion': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['version'],
                    'appInfoName': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['name'],
                    'vnfdVersion': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['version']}
        else:    
            result = {'appdId': self.mec_data['topology_template']['node_templates']['VNF']["properties"]['descriptor_id'],
                    'appProvider': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['provider'],
                    'appProductName': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['provider_name'],
                    'type': 'app',
                    'appName': self.mec_data['topology_template']['node_templates']['VNF']["properties"]['product_name'],
                    'appSoftwareVersion': self.mec_data['topology_template']['node_templates']['VNF']["properties"]['software_version'],
                    'appdVersion': self.mec_data['topology_template']['node_templates']['VNF']["properties"]['descriptor_version'],
                    'mecVersion': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['version'],
                    'appInfoName': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['name'],
                    'appServiceRequired': self.mec_data['topology_template']['node_templates']['VDU']['artifacts']['app_service']['service_required'],
                    'appServiceProduced': self.mec_data['topology_template']['node_templates']['VDU']['artifacts']['app_service']['service_provider'],
                    'appFeatureRequired': self.mec_data['topology_template']['node_templates']['VDU']['artifacts']['app_service']['service_describe'],
                    'vnfdVersion': self.mec_data['topology_template']['node_templates']['VDU']['properties']['sw_image_data']['version']}
        print(result)
        return result
