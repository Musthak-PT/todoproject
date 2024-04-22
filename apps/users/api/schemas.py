from rest_framework import serializers

from apps.users.models import Users


class MyProfileListingApiSchemas(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ['email','full_name','phone','image']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data