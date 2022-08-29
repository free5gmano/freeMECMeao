import os

from rest_framework import serializers
from utils.file_manipulation import create_dir
from .models import *

nsd_base_path = os.getcwd() + "/NSD/"
create_dir(nsd_base_path)

class NsdInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = NsdInfo
        fields = '__all__'

    def create(self, validated_data):
        nsd = NsdInfo.objects.create(**validated_data)
        path = '{}{}'.format(nsd_base_path, nsd.id)
        content_path = 'nsd_content'
        create_dir(path + "/" + content_path)
        return nsd
