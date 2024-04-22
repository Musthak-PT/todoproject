import logging
import threading
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from apps.users.admin_mail import admin_register_completion_mail
from apps.users.models import Group, Users
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from todo import settings
from todo.helpers.mail_fuction import SendEmails
from todo.helpers.signer import URLEncryptionDecryption
from todo.helpers.helper import get_object_or_none
from django.contrib.auth.tokens import default_token_generator

logger = logging.getLogger(__name__)


class AdminsView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/user/admins/admin.html'
        self.context['title'] = 'Admins'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Admins", "route" : '','active' : True});


class LoadAdminsDatatable(BaseDatatableView):
    
    
    order_columns = ['id','email', 'image', 'full_name', 'is_active']
    
    def get_initial_queryset(self):
        if not self.request.user.is_superuser:
            model = Users.objects.filter(is_superuser=False)
        else: 
            model = Users.objects.all()
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return model.filter(is_active=1).exclude(is_admin=0)
        elif filter_value == '2':
            return model.filter(is_active=0).exclude(is_admin=0)
        else:
            return model.all().exclude(is_admin=0)


    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(email__icontains=search) | Q(full_name__icontains=search) )

        """Advanced filtering

        Returns:
            _type_: _description_
        """
        filter_email = self.request.POST.get('email', None)
        
        
        if filter_email is not None:
            users_datas = filter_email.split(' ')
            qs_params = None
            for part in users_datas:
                q = Q(email__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        
        return qs
    

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'            : escape(item.id),
                'full_name'     : escape(item.full_name),
                'email'         : escape(item.email),
                'phone'         : escape(item.phone),
                'is_active'     : escape(item.is_active),
                'image'         : escape(item.image.url),
                'created_date'  : item.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)),
                'super_user'    : escape(item.is_superuser)
           

            })
        return json_data
    
    
@method_decorator(login_required, name='dispatch')
class DestroyAdminsRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            users_ids = request.POST.getlist('ids[]')
            if users_ids:
                Users.objects.filter(id__in=users_ids).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
    

class AdminCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.context['title'] = 'Admin'
        self.action = "Create "
        self.template = 'admin/user/admins/create-or-update.html'


    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        
        if id:
            
            self.action = "Update "
            user = get_object_or_404(Users, id=id)
            self.context['admins'] = user
            active_groups = Group.objects.filter(id__in=user.user_groups.all().values_list('id', flat=True)).all().values_list('id', flat=True)
            self.context['active_groups'] = active_groups
            
            
        self.context['groups'] = Group.objects.all()
        self.generateBreadcrumbs()         
        return render(request, self.template , context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Users", "route": reverse('admins:admins.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Admin".format(self.action), "route": '', 'active': True})



    def post(self, request, *args, **kwargs):
        
        admin_id = request.POST.get('admin_id', None)
        try:
            groups = request.POST.getlist('groups')
            
            remove_groups = []
            
            if admin_id:
                
                self.action = 'Updated'
                admin = get_object_or_404(Users, id=admin_id)
                active_groups = Users.objects.get(id=admin_id).user_groups.all().values_list('id',flat=True)
                remove_groups = [item for item in active_groups if str(item) not in groups]
                [groups.remove(str(item)) for item in active_groups if str(item) in groups]
                
            else:
                admin = Users()
            
            if request.FILES.__len__() != 0:
                if request.POST.get('admin_image', None) is None:
                    admin.image = request.FILES.get('admin_image')
            
            admin.is_active = 0 if request.POST.get('admin_status',0) == ''  else  int(request.POST.get('admin_status',0))
            admin.full_name = request.POST.get('full_name', None)            
            admin.email     = request.POST.get('email', None)
            admin.phone    = request.POST.get('mobile', None)            
            admin.user_type = '1'
            if len(request.POST.get('password')) != 0:
                admin.password = make_password(request.POST.get('password'))
            admin.is_admin  = True
            admin.save()
            current_password = request.POST.get('password')
            email  = request.POST.get('email', None)
            for group in groups:
                group_instance = get_object_or_none(Group,id=group)
                if group_instance is not None:
                    group_instance.custom_group_set.add(admin)
            for remove_group in remove_groups:
                remove_group_instance = get_object_or_none(Group,id=remove_group)
                if remove_group_instance is not None:
                    remove_group_instance.custom_group_set.remove(admin)
            admin_register_completion_mail(request, admin, current_password, email)
            messages.success(request, f"Data Successfully "+ self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if admin_id is not None and admin_id != '':
                return redirect('admins:admins.update', id = URLEncryptionDecryption.dec(int(admin_id)) )   
            return redirect('admins:admins.create')
        return redirect('admins:admins.index')


class CheckEmailExistRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, **kwargs):
        try:
            email = request.POST.get('email',None)
            id = request.POST.get('instance_id', None)
            check_email   = Users.objects.filter(email=email)
            if check_email is not None and id:
                check_email = check_email.exclude(pk=id)
            if check_email.exists():
                self.response_format['status_code']=100
                self.response_format['message']= 'Email Already Exist'
            else:
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    
class CheckMobileExistRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, **kwargs):
        try:
            mobile = request.POST.get('mobile', None)
            id = request.POST.get('instance_id', None)
            check_mobile = Users.objects.filter(phone=mobile)
            if check_mobile is not None and id:
                check_mobile = check_mobile.exclude(pk=id)
            if check_mobile.exists():
                self.response_format['status_code'] = 100
                self.response_format['message'] = 'Mobile Number Already Exists'
            else:
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as es:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    
class ActiveInactiveAdminStatus(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Users.objects.get(id = instance_id)
            if instance_id:
                if instance.is_active:
                    instance.is_active = False
                else:
                    instance.is_active =True
                instance.save()
                self.response_format['status_code']=200
                self.response_format['message']= 'Success'
                
        except Exception as es:
            self.response_format['message']='error'
            self.response_format['error'] = str(es)
        return JsonResponse(self.response_format, status=200)
    
    
"""-----------------Change Password--------------------------"""

class AdminChangePasswordView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        self.context = {"breadcrumbs" : []}
        self.context['title'] = 'Admin'
        self.action = "Change "
        self.template = 'admin/user/admins/password-change.html'
        
        
    def get(self, request, *args, **kwargs):
        self.context['groups'] = Group.objects.all()
        self.generateBreadcrumbs()         
        return render(request, self.template , context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Users", "route": reverse('admins:admins.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{} Admin".format(self.action), "route": '', 'active': True})


    def post(self, request, **kwargs):
        try:
            password = request.POST.get('password', None)
            confirm_password = request.POST.get('confirm_password', None)
            
            if password and confirm_password and password == confirm_password:
                # Retrieve the user instance using the model
                instance = get_object_or_none(Users, id=request.user.id)
                
                if instance is not None:
                    instance.password = make_password(password)
                    instance.save()
                    self.response_format['status_code'] = 200
                    self.response_format['message'] = 'Success'
            else:
                self.response_format['status_code'] = 400
                self.response_format['message'] = 'New Password and confirm password are not the same'
                
        except Exception as es:
            self.response_format['status_code'] = 500  # Internal Server Error
            self.response_format['message'] = str(es)

        return JsonResponse(self.response_format, status=200)
    
    
"""-------------------------------ForGotPassword sections---------------------------"""

class AdminForgotPasswordPasswordView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        self.context = {"breadcrumbs" : []}
        self.context['title'] = 'Admin'
        self.action = "Change "
        self.template = 'admin/user/admins/forgotpassword/for-got-password.html'
        
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template , context=self.context)
    

    def post(self, request, **kwargs):
        try:
            email = request.POST.get('email', None)
        
            if email is not None:
                user_instance = get_object_or_none(Users,email=email)
                
                if user_instance is not None:
                    subject = "Password Reset Request "
                    context = {
                    "email"                             : email,
                    'domain'                            : settings.EMAIL_DOMAIN,
                    "uid"                               : URLEncryptionDecryption.enc(user_instance.id),
                    "user"                              : user_instance,
                    'token'                             : default_token_generator.make_token(user_instance),
                    'protocol'                          : 'https',
                    'forgot_password_page_url'          : request.build_absolute_uri(reverse('admins:admin.reset_change_password')),
                    }
                    send_email = SendEmails()
                    mail_sending=threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/password/admin_forgot_password.html',settings.EMAIL_HOST_USER, user_instance.email))
                    mail_sending.start()

                    self.response_format['status_code'] = 200
                    self.response_format['message'] = 'Email send successfully and please check the mail'
                else:
                    self.response_format['status_code'] = 400
                    self.response_format['message'] = 'User not found'
            else:
                self.response_format['status_code'] = 400
                self.response_format['message'] = 'Email not provided'

        except Exception as es:
            self.response_format['status_code'] = 500  # Internal Server Error
            self.response_format['message'] = str(es)

        return JsonResponse(self.response_format, status=200)

    
    
"""----------------- RESET PASSWORD-----------------------"""

class AdminResetPasswordView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        self.context = {"breadcrumbs" : []}
        self.context['title'] = 'Admin'
        self.action = "Change "
        self.template = 'admin/user/admins/forgotpassword/reset-password.html'
        
        
    def get(self, request, *args, **kwargs):
        self.context['uidb64'] = kwargs.get('uidb64')
        self.context['token'] = kwargs.get('token')
        return render(request, self.template , context=self.context)
    
    def post(self, request, **kwargs):
        try:
            uidb64 = request.POST.get('uidb64')
            token = request.POST.get('token')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            user_id = URLEncryptionDecryption.dec(uidb64)
            user_instance = get_object_or_none(Users, id=user_id)
            if user_instance is not None and default_token_generator.check_token(user_instance, token):
                if password and confirm_password and password == confirm_password:
                    user_instance.password = make_password(password)
                    user_instance.save()
                    self.response_format['status_code'] = 200
                    self.response_format['message'] = 'Password reset successfully'
                else:
                    self.response_format['status_code'] = 400
                    self.response_format['message'] = 'New Password and confirm password do not match'
            else:
                self.response_format['status_code'] = 400
                self.response_format['message'] = 'Invalid user or token'
                
        except Exception as es:
            self.response_format['status_code'] = 500  # Internal Server Error
            self.response_format['message'] = str(es)

        return JsonResponse(self.response_format, status=200)