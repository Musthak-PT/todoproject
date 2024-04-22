import logging
from rest_framework.response import Response
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from apps.users.api.schemas import MyProfileListingApiSchemas
from apps.users.api.serializers import CreateOrUpdateUserProfileSerializers, ChangePasswordSerializers
from apps.users.models import Users
from todo.helpers.helper import get_object_or_none
from todo.helpers.response import ResponseInfo
from todo.helpers.custom_messages import _success
from django.db.models import Q
logger = logging.getLogger(__name__)



class CreateOrUpdateUserProfileManagement(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateUserProfileManagement, self).__init__(**kwargs)

    serializer_class = CreateOrUpdateUserProfileSerializers

    @swagger_auto_schema(tags=["User Profile"])
    def post(self, request):
        try:
            serializer = self .serializer_class(data=request.data,context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            instance = serializer.validated_data.get('instance_id',None)
            serializer = self.serializer_class(instance, data=request.data, context={'request': request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class GetMyProfileListingApiView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetMyProfileListingApiView, self).__init__(**kwargs)

    serializer_class    = MyProfileListingApiSchemas
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(tags=["User Profile"],)
    def get(self, request, *args, **kwargs):
        queryset = get_object_or_none(Users,id=request.user.id)
        serializer = self.serializer_class(queryset, context={'request': request})
        self.response_format['status'] = True
        self.response_format['data'] = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)
  
#------------Reset password----------------
class ChangePasswordApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ChangePasswordApiView, self).__init__(**kwargs)

    serializer_class = ChangePasswordSerializers
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["Reset Password(Web)"])
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