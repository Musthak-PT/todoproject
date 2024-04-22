from rest_framework import serializers
from django.contrib.auth.models import Permission








class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source='content_type.app_label')
    content_model = serializers.CharField(source='content_type.model')
    
    class Meta:
        model = Permission
        fields = ['id','name','content_type','content_model','codename','label']


