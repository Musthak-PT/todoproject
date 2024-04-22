from drf_yasg import openapi
import logging
from apps.users.models import Users
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from todo.helpers.custom_messages import _account_tem_suspended,_invalid_credentials
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
import json
from todo.response import ResponseInfo
from apps.authentication.api.serializers import UserForgotPasswordChangeSerializer, RefreshTokenSerializer, UpdateCustomerProfilePictureSerializer, UserRegisterSerializer, LoginSerializer, LogoutSerializer, OTPSerializer, UserRegisterUpdateSerializer, CustomerRegistrationSerializer, UpdateCustomerProfileSerializer, CustomerLoginSerializer, UserChangePasswordSerializers
from apps.authentication.api.schemas import FinalRegistrationPostSchema, FinalRegistrationSchema, LoginPostSchema, LoginSchema, RegisterPostSchema, RegisterSchema, UsersSchema, VerifyOTPPostSchema,GetAllCustomerApiViewSchema, AdminLoginSchema
from todo import settings
from todo.helpers.helper import DataEncryption
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import generics
from todo.helpers.custom_messages import _success
from rest_framework import filters
from apps.authentication.api.customer_mail import customer_registeration_mail_send
from apps.authentication.api.schemas import CustomerProfileSchema, UserAdminForgotPasswordResponseSchema, GetProfileCustomerSchemas, GetProfilePictureSchemas
import threading
from todo.helpers.mail_fuction import SendEmails
from todo.helpers.custom_messages import _success, _record_not_found
from todo.helpers.signer import URLEncryptionDecryption
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class RegisterAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RegisterAPIView, self).__init__(**kwargs)

    serializer_class = RegisterPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user_data = request.data
            user_data.update({'is_active' : False})
            serializer = UserRegisterSerializer(data=user_data)
            if serializer.is_valid():
                if serializer.save():
                    data = {'user': serializer.data, 'errors': {}}
                    self.response_format['status_code'] = status.HTTP_201_CREATED
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_201_CREATED)
                else:
                    self.response_format['status_code'] = status.HTTP_200_OK
                    data = {'user': serializer.data, 'errors': {}}
                    self.response_format["data"] = data
                    self.response_format["status"] = True
                    return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                data = {'user': {}, 'errors': serializer.errors}
                self.response_format["data"] = data
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FinalRegistrationAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(FinalRegistrationAPIView, self).__init__(**kwargs)

    serializer_class = FinalRegistrationPostSchema

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user_data = request.data
            serializer = UserRegisterUpdateSerializer(data=user_data)
            if serializer.is_valid():
                if serializer.update():
                    data = request.data
                    password = data.get('password', '')
                    user_obj = Users.objects.get(pk=data.get('pk', ''))
                    user = auth.authenticate(username=user_obj.email, password=password)
                    if user:
                        refresh = RefreshToken.for_user(user)
                        serializer = FinalRegistrationSchema(user)
                        data = {'user': serializer.data, 'errors': {}, 'token': str(
                            refresh.access_token), 'refresh': str(refresh)}
                        self.response_format['status_code'] = 200
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        return Response(self.response_format, status=status.HTTP_201_CREATED)
                    else:
                        self.response_format['status_code'] = 106
                        data = {'user': serializer.data, 'errors': {}, 'token': '', 'refresh': ''}
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        return Response(self.response_format, status=status.HTTP_201_CREATED)
                else:
                    self.response_format['status_code'] = 102
                    data = {'user': {}, 'errors': {},
                            'token': '', 'refresh': ''}
                    self.response_format["data"] = data
                    self.response_format["status"] = False
                    return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.response_format['status_code'] = 102
                data = {'user': {}, 'errors': serializer.errors,
                        'token': '', 'refresh': ''}
                self.response_format["data"] = data
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)

        

# class LoginAPIView(GenericAPIView):
#     def __init__(self, **kwargs):
#         self.response_format = ResponseInfo().response
#         super(LoginAPIView, self).__init__(**kwargs)

    # serializer_class = LoginPostSchema

#     @swagger_auto_schema(tags=["Authorization"])
#     def post(self, request):
#         try:
#             data = request.data
#             email = data.get('email', '')
#             password = data.get('password', '')
#             user = auth.authenticate(username=email, password=password)            
#             if user:
#                 serializer = LoginSchema(user)

#                 if not user.is_active:
#                     data = {'user': {}, 'token': '', 'refresh': ''}
#                     self.response_format['status_code'] = status.HTTP_202_ACCEPTED
#                     self.response_format["data"] = data
#                     self.response_format["status"] = True
#                     self.response_format["message"] = 'Account Temparary suspended, contact admin'
#                     return Response(self.response_format, status=status.HTTP_200_OK)
#                 else:
#                     refresh = RefreshToken.for_user(user)
#                     data = {'user': serializer.data, 'token': str(
#                         refresh.access_token), 'refresh': str(refresh)}
#                     self.response_format['status_code'] = status.HTTP_200_OK
#                     self.response_format["data"] = data
#                     self.response_format["status"] = True
#                     return Response(self.response_format, status=status.HTTP_200_OK)

#             else:
#                 self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
#                 self.response_format["message"] = 'Invalid credentials'
#                 self.response_format["status"] = False
#                 return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

#         except Exception as e:
#             pass
#             self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
#             self.response_format['status'] = False
#             self.response_format['message'] = str(e)
#             return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Start Login 
class LoginAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)
        
    serializer_class = LoginSerializer
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            email    = serializer.validated_data.get('email', '')
            password = serializer.validated_data.get('password', '')
            try:
                user_instance = Users.objects.get(email=email)
            except:
                user_instance = None
            if user_instance:
                user = auth.authenticate(request=request, username=user_instance.email, password=password)
                
                if user:
                    serializer = LoginSchema(user, context={"request": request})
                    if not user.is_active:
                        data = {'user': {}, 'token': '', 'refresh': ''}
                        self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                        self.response_format["data"] = data
                        self.response_format["status"] = False
                        self.response_format["message"] = _account_tem_suspended
                        return Response(self.response_format, status=status.HTTP_200_OK)
                    else:
                        final_out         = json.dumps(serializer.data)
                        key               = settings.E_COMMERCE_SECRET        
                        encrypted_data    = DataEncryption.encrypt(key, final_out)
                        access_tokens     = AccessToken.for_user(user)
                        refresh_token     = RefreshToken.for_user(user)             
                  
                        
                        data = {'user': encrypted_data, 'token': str(access_tokens), 'refresh': str(refresh_token)}
                        self.response_format['status_code'] = status.HTTP_200_OK
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        self.response_format["message"] = _success

                        return Response(self.response_format, status=status.HTTP_200_OK)

                else:
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format["message"] = _invalid_credentials
                    self.response_format["status"] = False
                    return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = _invalid_credentials
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# End Login

class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
        
        
class RefreshTokenView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefreshTokenSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RefreshTokenView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            refresh = RefreshToken.for_user(user)
            data = {'token': str(
                refresh.access_token), 'refresh': str(refresh)}
            self.response_format['status_code'] = 200
            self.response_format["data"] = data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)
        
#----start create or update customer registration------------        
class CreateOrUpdateCustomerRegistrationApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateCustomerRegistrationApiView, self).__init__(**kwargs)
    
    serializer_class = CustomerRegistrationSerializer
    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            instance = serializer.save()
            customer_registeration_mail_send(request, instance)

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = serializer.errors
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End customer registeration
        
#Listing Customers
class GetAllCustomerApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllCustomerApiView, self).__init__(**kwargs)

    queryset         = Users.objects.filter(user_type=2).order_by('-id')
    serializer_class = GetAllCustomerApiViewSchema
    filter_backends  = [filters.SearchFilter]
    # permission_classes = [IsAuthenticated]
    search_fields    = ['email', 'first_name', 'last_name', 'phone']

    id = openapi.Parameter('id', openapi.IN_QUERY,
                                type=openapi.TYPE_INTEGER, required=False, description="Enter Customer id")

    @swagger_auto_schema(tags=["Authorization"], manual_parameters=[id])
    def get(self, request, *args, **kwargs):
        queryset   = self.filter_queryset(self.get_queryset())
        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
            
        serializer = self.serializer_class(queryset, many=True)
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)

#update customer profile
class UpdateProfileCustomerApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateProfileCustomerApiView, self).__init__(**kwargs)
    
    serializer_class = UpdateCustomerProfileSerializer
    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            instance = Users.objects.get(id=request.user.id)
            customer_schema = CustomerProfileSchema(instance, context={"request": request})

            serializer = self.serializer_class(instance, data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            data ={
                "id"              : instance.id,
                "slug"            : instance.slug,
                "full_name"       : instance.full_name,
                "email"           : instance.email,
                "phone"           : str(instance.phone),
                "alter_number"    : str(instance.alternative_phone)

            }
            final_out         = json.dumps(customer_schema.data)
            key               = settings.E_COMMERCE_SECRET
                        
            encrypted_data    = DataEncryption.encrypt(key, final_out)
            data = {'encrypt_user': encrypted_data, 'user_data':data}
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["data"] = data  # Return all data after the update
            self.response_format["status"] = True

            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Users.DoesNotExist:
            self.response_format['status_code'] = status.HTTP_404_NOT_FOUND
            self.response_format['status'] = False
            self.response_format['message'] = "User not found"
            return Response(self.response_format, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#End update of customer
#Update profile picture
class UpdateProfilePictureCustomerApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateProfilePictureCustomerApiView, self).__init__(**kwargs)
    
    serializer_class = UpdateCustomerProfilePictureSerializer
    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            instance = Users.objects.get(id=request.user.id)
            serializer = self.serializer_class(instance, data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["data"] = serializer.data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End Update profile picture
#Customer login
class CustomerLoginView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CustomerLoginView, self).__init__(**kwargs)
        
    serializer_class = CustomerLoginSerializer
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            email    = serializer.validated_data.get('email', '')
            password = serializer.validated_data.get('password', '')
            try:
                user_instance = Users.objects.get(email=email)
            except:
                user_instance = None
            if user_instance:
                user = auth.authenticate(request=request, username=user_instance.email, password=password)
                
                if user:
                    serializer = AdminLoginSchema(user, context={"request": request})
                    if not user.is_active:
                        data = {'user': {}, 'token': '', 'refresh': ''}
                        self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                        self.response_format["data"] = data
                        self.response_format["status"] = False
                        self.response_format["message"] = _account_tem_suspended
                        return Response(self.response_format, status=status.HTTP_200_OK)
                    else:
                        final_out         = json.dumps(serializer.data)
                        key               = settings.E_COMMERCE_SECRET
                        
                        encrypted_data    = DataEncryption.encrypt(key, final_out)
                        access_tokens     = AccessToken.for_user(user)
                        refresh_token     = RefreshToken.for_user(user)             
                        
                        data = {'user': encrypted_data, 'token': str(access_tokens), 'refresh': str(refresh_token)}
                        self.response_format['status_code'] = status.HTTP_200_OK
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        self.response_format["message"] = _success
                        return Response(self.response_format, status=status.HTTP_200_OK)

                else:
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format["message"] = _invalid_credentials
                    self.response_format["status"] = False
                    return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = _invalid_credentials
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End of customer login

# Start Forgot Password
class UserAdminForgotPasswordAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UserAdminForgotPasswordAPIView, self).__init__(**kwargs)
        
    serializer_class = UserAdminForgotPasswordResponseSchema
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user_email      = request.data.get('user_email', None)
            user_instance   = Users.objects.get(email=user_email)
            if user_instance is None:
                self.response_format['status_code'] = status.HTTP_404_NOT_FOUND
                self.response_format['status']      = False
                self.response_format['message']     = _record_not_found
                return Response(self.response_format, status=status.HTTP_404_NOT_FOUND)
            else:

                subject = "Password Reset Requested"
                context = {
                    "email"                             : user_email,
                    'domain'                            : settings.EMAIL_DOMAIN,
                    "uid"                               : URLEncryptionDecryption.enc(user_instance.id),
                    "user"                              : user_instance,
                    'token'                             : default_token_generator.make_token(user_instance),
                    'protocol'                          : 'https',
                    'admin_forgot_password_page_url'    : settings.ADMIN_FORGOT_PASSWORD_PAGE_URL if user_instance.user_type == '1' else settings.CUSTOMER_FORGOT_PASSWORD_PAGE_URL,
                }
                try:
                    send_email = SendEmails()
                    mail_sending=threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/passwords/admin_forgot_password.html', settings.EMAIL_HOST_USER, user_email))
                    mail_sending.start()
                    
                    self.response_format['status']      = True
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format['message']     = "The email has been sent successfully. Please check your mail."
                    return Response(self.response_format, status=status.HTTP_200_OK)

                except Exception as es:
                    self.response_format['status']      = False
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format['message']     = 'Please enter valid email'
                    return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as es:
            self.response_format['status']      = False
            self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
            self.response_format['message']     = 'Please enter valid email'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#End

#start
class AdminPasswordResetConfirmView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(AdminPasswordResetConfirmView, self).__init__(**kwargs)
    
    serializer_class = UserForgotPasswordChangeSerializer
    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request, *args, **kwargs):
        
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            uid                 = serializer.validated_data.get('uid', None)
            token               = serializer.validated_data.get('token', None)
            confirm_password    = serializer.validated_data.get('confirm_password', None)
            new_password        = serializer.validated_data.get('new_password', None)
        try:
            client_id = URLEncryptionDecryption.dec(uid)
            client = Users.objects.get(id=client_id)
            verify = default_token_generator.check_token(client, token)
            if verify:
                if client:
                    if new_password == confirm_password:
                        client.set_password(new_password)
                        client.save()
                        self.response_format['message']     = 'Password Changed'
                        self.response_format['status_code'] = 100
                    else:
                        self.response_format['message'] = 'Password not Matching'
            else:
                self.response_format['status_code'] = 109
                self.response_format['message']     = 'Please try again'
        except:
            self.response_format['message'] = 'User not found, try again'
            
        return JsonResponse(self.response_format, status=200)  
#Listing of the updated profile details
class GetProfileCustomerApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetProfileCustomerSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug']

    @swagger_auto_schema(tags=["Authorization"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, many=True)

        response_format = ResponseInfo().response
        response_format['status'] = True
        response_format['data'] = serializer.data
        response_format['status_code'] = status.HTTP_200_OK
        return Response(response_format, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Users.objects.filter(pk=self.request.user.pk).order_by('-id')    
# End
class GetProfilePictureApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetProfilePictureSchemas
    filter_backends = [filters.SearchFilter]
    search_fields = ['slug']

    @swagger_auto_schema(tags=["Authorization"])
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)

        response_format = ResponseInfo().response
        response_format['status'] = True
        response_format['data'] = serializer.data
        response_format['status_code'] = status.HTTP_200_OK
        return Response(response_format, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Users.objects.filter(pk=self.request.user.pk).order_by('-id')

# Start Reset Password
class ChangePasswordApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ChangePasswordApiView, self).__init__(**kwargs)

    serializer_class = UserChangePasswordSerializers
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Authorization"])
    def put(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            serializer = self.serializer_class(user, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.response_format['status_code'] = status.HTTP_201_CREATED
                self.response_format["message"] = _success
                self.response_format["status"] = True
                return Response(self.response_format, status=status.HTTP_201_CREATED)
            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# End Reset Password