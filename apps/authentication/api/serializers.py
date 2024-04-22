from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.hashers import make_password, check_password
from apps.users.models import Users
from todo.helpers.helper import ConvertBase64File
from uuid import uuid4

class UserRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255, min_length=4)
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=255, min_length=4)
    last_name = serializers.CharField(max_length=255, min_length=2)
    is_active = serializers.BooleanField(default = True)

    class Meta:
        model = Users
        fields = ['id','phone', 'email', 'first_name','last_name','is_active']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        email = attrs.get('email', '') 
        
        
        if Users.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                {'phone': ('Phone number is already in use')})
            
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('email address is already in use')})
            
        return super().validate(attrs)

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)


class UserRegisterUpdateSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    password = serializers.CharField(max_length=65, min_length=8)
    username = serializers.CharField(max_length=255, min_length=4)
    confirm_password = serializers.CharField(max_length=65, min_length=8)

    class Meta:
        model = Users
        fields = ['password', 'username','pk']

    def validate(self, attrs):
        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', None)
        pk = attrs.get('pk', None)

        if confirm_password != password:
            raise serializers.ValidationError(
                {'password_mismatch': ('password an confirm password are not match')})
        
        
        if not Users.objects.filter(pk=pk).exists():
            raise serializers.ValidationError(
                {'not_found': ('user not found in our system.')})
            
      
        return super().validate(attrs)
    
    

    def update(self):
        pk = self.data.get('pk')
        if pk:
            user = Users.objects.get(pk=pk)
            user.username = self.data.get('username')
            user.set_password(self.data.get('password'))
            user.is_active = True
            user.save()
            return True
        
        return False
        

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = Users
        fields = ['username', 'password']


class OTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=255, min_length=4)

    class Meta:
        model = Users
        fields = ['otp']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
# Start Login
class LoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta:
        model = Users
        fields = ['email','password']
    
    def validate(self, attrs):
        return super().validate(attrs)    
    
# End Login
#--------Start Customer registeration----------
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    full_name           = serializers.CharField(required=True)
    email               = serializers.EmailField(required=True)
    password            = serializers.CharField(required=True)
    confirm_password    = serializers.CharField(required=True)
    
    class Meta:
        model = Users
        fields = ['full_name', 'email', 'password', 'confirm_password', ]
        
    def validate(self, attrs):
     
        email               = attrs.get('email')
        password            = attrs.get('password')
        confirm_password    = attrs.get('confirm_password')
        instance_id         = attrs.get('instance_id')
        
        if not instance_id:
            if email and Users.objects.filter(email=email).exists():
                raise serializers.ValidationError({"error": ['Sorry, that email address is already in exists!']})
            if password != confirm_password:
                raise serializers.ValidationError({"error": ['Sorry, Password do not match!']})
            return super().validate(attrs)
    
    def create(self, validated_data):
        request               = self.context.get('request')
        instance              = Users()
        instance.full_name    = validated_data.get('full_name', None)
        instance.email        = validated_data.get('email', None)
        password              = validated_data.get('password', None)
        confirm_password      = validated_data.get('confirm_password', None)
        if password == confirm_password:
            instance.password = make_password(password)
        instance.user_type    = 2
        instance.save()
        return instance
#End registeration
#update customer profile
    
class UpdateCustomerProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, required=False)
    phone     = serializers.CharField(required=False)
    alternative_phone_number = serializers.CharField(required=False)
    
    class Meta:
        model = Users
        fields = ['full_name', 'phone', 'alternative_phone_number']
    
    def validate_phone(self, value):
        # Check if the phone number already exists for a different user
        existing_user = Users.objects.exclude(id=self.instance.id).filter(phone=value).first()
        if existing_user:
            raise serializers.ValidationError('This phone number is already in use!')
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.alternative_phone = validated_data.get('alternative_phone_number', instance.alternative_phone)
        instance.save()
        return instance
#End
#Update profile picture
    
class UpdateCustomerProfilePictureSerializer(serializers.ModelSerializer):
    image               = serializers.CharField(required=False)
    
    class Meta:
        model  = Users
        fields = ['image']
        
    def validate(self, attrs):
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        request       = self.context.get('request')
        profile_pic   = validated_data.get('image', None)
        if validated_data.get('image', None):
            extension           = ConvertBase64File.base64_file_extension(request, profile_pic)
            output_schema_xsd   = ConvertBase64File.base64_to_file(request, profile_pic)
            unique_filename     = f'{uuid4()}.{extension}'                    
            instance.image.save(unique_filename, output_schema_xsd, save = True)
        instance.save()
        return instance
    
#End Update profile picture
#Customer login serializer
class CustomerLoginSerializer(serializers.ModelSerializer):
    email       = serializers.EmailField(required=True)
    password    = serializers.CharField(required=True)
    
    class Meta:
        model  = Users
        fields = ['email', 'password']
        
    def validate(self, attrs):
        return super().validate(attrs) 
#End of Customer login

class UserForgotPasswordChangeSerializer(serializers.Serializer):
    
    new_password        = serializers.CharField(required=True)
    confirm_password    = serializers.CharField(required=True)
    uid                 = serializers.CharField(required=True)
    token               = serializers.CharField(required=True)
    
    def validate(self,attrs):
        return super().validate(attrs) 


# Start Reset Password
class UserChangePasswordSerializers(serializers.ModelSerializer):
    old_password     = serializers.CharField(required=True)
    new_password     = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = Users
        fields = ['old_password', 'confirm_password', 'new_password']        

    def validate(self, attrs):
        user_instance       = self.instance
        old_password        = attrs.get('old_password')
        confirm_password    = attrs.get('confirm_password')
        new_password        = attrs.get('new_password')
        
        if user_instance:
            user_password_instance = user_instance.password
            checking_password      = check_password(old_password, user_password_instance)
            if not checking_password:
                raise serializers.ValidationError({"old_password": ['Sorry, The old Password is not correct!']})
            elif new_password != confirm_password:
                raise serializers.ValidationError({"Password mismatch": ['Sorry, New password and Confirm password do not match!']})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        new_password = make_password(validated_data.get('new_password', None))
        if new_password:
            instance.password = new_password
        instance.save()
        return instance 