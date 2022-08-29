from utils.file_manipulation import sha256_hash
import requests
import json
import yaml
from utils.file_manipulation import read_yaml_file,load_yaml_file
from kube5gMEAO.settings import NFVO_PATH
class Mv1Agent :
    def __init__(self, *args, **kwargs):
        self.check_url = NFVO_PATH+"mecnfvo/mecplatform"
        self.platform_url=NFVO_PATH+"mecnfvo/mecplatformlcm"
        self.app_url = NFVO_PATH+"mecnfvo/mecapp"
        self.repo_url = NFVO_PATH+"mecnfvo/chart"
        self.headers = {'Content-Type': 'application/json'}
        self.mec_app_json=dict()
        self.mec_platform_json=dict()
        self.cluster_name=kwargs['cluster_name']
        self.mec_platform_name=kwargs['mec_platform_name']
    def checkMEC(self):
        check_mec_json = dict()
        check_mec_json['cluster'] = self.cluster_name
        check_mec_json['mec_platform'] = self.mec_platform_name
        return requests.post(self.check_url,headers=self.headers,data=json.dumps(check_mec_json))
    def createMEC(self):
        check_mec_json = dict()
        check_mec_json['cluster'] = self.cluster_name
        check_mec_json['mec_platform'] = self.mec_platform_name
        return requests.post(self.platform_url,headers=self.headers,data=json.dumps(check_mec_json))
    def addHelmChart(self,repoName,repoUrl):
        self.mec_app_json['cluster']=self.cluster_name
        self.mec_app_json['mec_platform']=self.mec_platform_name
        self.mec_app_json['repoName']=repoName
        self.mec_app_json['repoUrl']=repoUrl
        return requests.post(self.repo_url,headers=self.headers,data=json.dumps(self.mec_app_json))
    def createMECApp(self,repoName,mecApp,mecName,serviceType,service):
        self.mec_app_json['repoName']=repoName
        self.mec_app_json['cluster']=self.cluster_name
        self.mec_app_json['mec_platform']=self.mec_platform_name
        self.mec_app_json['mecApp']=mecApp
        self.mec_app_json['mecName']=mecName
        self.mec_app_json['mecPlatformServiceType']=serviceType
        self.mec_app_json['mecPlatformServiceFunction']=service
        print(self.mec_app_json)
        return requests.post(self.app_url,headers=self.headers,data=json.dumps(self.mec_app_json))
    
    def createMECPlatform(self):
        return requests.post(self.check_url,headers=self.headers,data=json.dumps(self.mec_platform_json))
    