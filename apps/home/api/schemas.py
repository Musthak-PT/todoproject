from rest_framework import serializers
from apps.home.models import CompanyProfilePdf, Department, OurClients, OurProjects, OurProjectsImages, OurServices, OurServicesPoints, ProjectDomain


"""----------------------------OUR PROJECT------------------------------"""

class OurProjectsApiImagesApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = OurProjectsImages
        fields = ['id','image']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class OurProjectsApiListingApiSchemas(serializers.ModelSerializer):
    project_image   = serializers.SerializerMethodField('get_project_images')
    class Meta:
        model = OurProjects
        fields = ['id','order','project_image','title','web_link','is_active']
        
    def get_project_images(self,data):
        request= self.context.get('request')
        images = OurProjectsImages.objects.filter(learn_campaign=data)
        image_serializer = OurProjectsApiImagesApiSchemas(images,many=True,context={'request': request})
        if image_serializer:
            return image_serializer.data
        return []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
"""----------------------------OUR CLIENTS------------------------------"""

class OurClientsApiListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = OurClients
        fields = ['id','client_logo','order','is_active']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

"""----------------------------OUR SERVICE------------------------------"""
class OurServicePointsApiListingApiSchemas(serializers.ModelSerializer):
    service = serializers.CharField(source='service.title',allow_null=True)
    class Meta:
        model = OurServicesPoints
        fields = ['id','service','title','description']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data


class OurServiceApiListingApiSchemas(serializers.ModelSerializer):
    service_points = serializers.SerializerMethodField('get_service_points')
    class Meta:
        model = OurServices
        fields = ['order','slug','id','title','full_name','url','is_popular','is_active','description_title','button_titile','service_image','description','is_main','service_points']

    def get_service_points(self,data):
        points = OurServicesPoints.objects.filter(service=data)
        service_points_serializer = OurServicePointsApiListingApiSchemas(points,many=True)
        if service_points_serializer:
            return service_points_serializer.data
        return []        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
class OurServiceChoiceApiListingApiSchemas(serializers.ModelSerializer):
    value = serializers.CharField(source="slug")
    label = serializers.CharField(source="title")
    class Meta:
        model = OurServices
        fields = ['value','label',]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

"""------------------------DEPARTMENT LISTING SCHEMAS----------------------- """

class DepartmentsChoiceApiListingApiSchemas(serializers.ModelSerializer):
    key = serializers.CharField(source="pk")
    value = serializers.CharField(source="title")
    class Meta:
        model = Department
        fields = ['key','value',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
"""------------------------DEPARTMENT LISTING SCHEMAS----------------------- """

class ProjectDomainChoiceApiListingApiSchemas(serializers.ModelSerializer):
    key = serializers.CharField(source="slug")
    value = serializers.CharField(source="title")
    class Meta:
        model = ProjectDomain
        fields = ['key','value',]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
    
"""------------------- COMPANY PROFILE RESPONSE SCHEMAS --------------------------------"""

class ComPanyProfilePdfListingApiSchemas(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfilePdf
        fields = ['id','title','file','is_active']


    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
