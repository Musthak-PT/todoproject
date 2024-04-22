from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password

from apps.users.models import Users


class CreateOrUpdateUserProfileSerializers(serializers.ModelSerializer):
    instance_id   = serializers.PrimaryKeyRelatedField(queryset = Users.objects.all(),required=False)
    full_name    = serializers.CharField(required=False)
    email         = serializers.EmailField(required=False)
    password      = serializers.CharField(required=False)
    phone         = serializers.CharField(required=False)
    
    class Meta:
        model = Users
        fields = ['instance_id','email','password','full_name','phone']
        
    def validate(self, attrs):
     
        phone    = attrs.get('phone')
        email    = attrs.get('email')
        instance_id    = attrs.get('instance_id')
        
        if not instance_id:
            if phone and email and Users.objects.filter(phone=phone, email=email).exists():
                raise serializers.ValidationError({"errors": ['Sorry, that phone number and email address is already in exists!']
                                                })
            
            if phone and Users.objects.filter(phone=phone).exists():
                raise serializers.ValidationError({"errors": ['Sorry, that phone number already exists!']})


            if email and Users.objects.filter(email=email).exists():
                raise serializers.ValidationError({"errors": ['Sorry, that email address already exists!']})
            
            return super().validate(attrs)
        else:
            if phone and email and Users.objects.filter(phone=phone, email=email).exclude(id=instance_id.id).exists():
                raise serializers.ValidationError({"errors": ['Sorry, that phone number and email address is already in exists!']
                                                })
            
            if phone and Users.objects.filter(phone=phone).exclude(id=instance_id.id).exists():
                raise serializers.ValidationError({"errors": ['Sorry, that phone number already exists!']})


            if email and Users.objects.filter(email=email).exclude(id=instance_id.id).exists():
                raise serializers.ValidationError({"errors": ['Sorry, that email address already exists!']})
            
            return super().validate(attrs)
        
    def create(self, validated_data):
        request               = self.context.get('request')
        instance              = Users()
        instance.full_name    = validated_data.get('full_name')
        instance.phone        = validated_data.get('phone')
        instance.email        = validated_data.get('email')
        password = validated_data.get('password')
        if password is not None :
            instance.password = make_password(password)
        instance.save()
        
        return instance
    
    def update(self, instance, validated_data):
        request               = self.context.get('request')
        if validated_data.get('full_name') is not None:
            instance.full_name   = validated_data.get('full_name')
            
        if validated_data.get('phone') is not None:
            instance.phone        = validated_data.get('phone')
            
        if validated_data.get('email') is not None:
            instance.email        = validated_data.get('email')
            
        password = validated_data.get('password')
        if password is not None :
            instance.password = make_password(password)
        instance.save()
        
        return instance

# Start Reset Password
class ChangePasswordSerializers(serializers.ModelSerializer):
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



