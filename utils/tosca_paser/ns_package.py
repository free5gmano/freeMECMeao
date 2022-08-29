from utils.file_manipulation import sha256_hash
import yaml
from utils.file_manipulation import read_yaml_file,load_yaml_file
class PackageNS():

    def __init__(self, path=None):
        self.tosca_metadata = read_yaml_file('{}TOSCA-Metadata/TOSCA.meta'.format(path))
        self.entry_definitions = self.tosca_metadata['Entry-Definitions']
        self.mec_ns_yaml_path=path + self.entry_definitions
        self.mec_ns_data=(load_yaml_file(path + self.entry_definitions))
        try :
            self.platform_name= self.mec_ns_data['topology_template']['node_templates']['NS']["properties"]['deployed_cluster']['platform_name']
        except:
            self.platform_name= "None"
        print(self.platform_name)
    def processing_data(self):
        
        result = {'nsdId': self.mec_ns_data['topology_template']['node_templates']['NS']["properties"]['descriptor_id'],
                  'nsdName': self.mec_ns_data['topology_template']['node_templates']['NS']["properties"]['name'],
                  'nsdVersion': self.mec_ns_data['topology_template']['node_templates']['NS']["properties"]['version'],
                  'nsdDesigner': self.mec_ns_data['topology_template']['node_templates']['NS']["properties"]['designer'],
                  'nsdInvariantId': self.mec_ns_data['topology_template']['node_templates']['NS']["properties"]['invariant_id'],
                  'deployedCluster': self.mec_ns_data['topology_template']['node_templates']['NS']["properties"]['deployed_cluster']['name'],
                  'platformName': self.platform_name,
                  'appPkgIds':list()}
        return result
    def get_constituent_vnfd(self):
        return self.mec_ns_data['topology_template']['node_templates']['NS']["properties"]['deployed_cluster']['constituent_appd']
