from django.contrib.auth.models import Permission
from rest_framework import serializers
from apps.users.models import Users


class RegisterPostSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email','phone','first_name','last_name']


class RegisterSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 
                  'first_name', 'last_name', 'is_admin', 'is_active', 'is_verified', 'is_superuser']




class FinalRegistrationPostSchema(serializers.Serializer):
    class Meta:
        model = Users
        fields = ['pk','password','confirm_password']


class FinalRegistrationSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone', 
                  'first_name', 'last_name', 'is_admin', 'is_active', 'is_verified', 'is_superuser']

class LoginPostSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email','password']
# class LoginSchema(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['email', 'phone', 'username',
#                   'first_name', 'last_name', 'is_admin', 'is_active', 'is_verified', 'is_superuser']

#------------------login schema------------------------------
class GetUserGroupsSerializer(serializers.ModelSerializer):
    
    value    =  serializers.IntegerField(source='pk')
    label    =  serializers.CharField(source='name')
    class Meta:
        model  = Permission
        fields = ['value','label']

class LoginSchema(serializers.ModelSerializer):
    user_groups = serializers.SerializerMethodField('get_user_groups')
    class Meta:
        model = Users
        fields = ['id','email','phone','is_active', 'user_groups']
        
    def get_user_groups(self, obj):
        return GetUserGroupsSerializer(obj.user_groups.all(), many=True).data
#-----------------------end here--------------------------

class UsersSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'phone','username',
                  'first_name', 'last_name', 'date_joined', 'is_admin', 'is_active', 'is_verified', 'is_superuser']



class VerifyOTPPostSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['otp']

#Listing of customers
class GetAllCustomerApiViewSchema(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = ['id', 'slug', 'full_name', 'email', 'phone','image', 'alternative_phone', 'date_joined']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
#End of listing of customers
#Login schema
class AdminLoginSchema(serializers.ModelSerializer):
    user_groups = serializers.SerializerMethodField('get_user_groups')
    class Meta:
        model = Users
        fields = ['id','email','phone', 'alternative_phone', 'full_name','is_active', 'user_groups']
        
    def get_user_groups(self, obj):
        return GetUserGroupsSerializer(obj.user_groups.all(), many=True).data
#End
class CustomerProfileSchema(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','slug','full_name','email','phone', 'alternative_phone']

class UserAdminForgotPasswordResponseSchema(serializers.ModelSerializer):
    user_email = serializers.EmailField(required=True)
    class Meta:
        model = Users
        fields = ['user_email']

class GetProfileCustomerSchemas(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'slug', 'email','full_name','phone','alternative_phone']

class GetProfilePictureSchemas(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['image']
