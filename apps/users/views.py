import json
from re import I, T
from django.contrib.auth.models import Group, Permission
import logging
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from apps.users.models import Users
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django_acl.models import Group,Role
from apps.users.schema import PermissionSerializer
from todo.helpers.helper import get_object_or_none
from todo.helpers.signer import URLEncryptionDecryption
logger = logging.getLogger(__name__)




class RoleView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/user/roles/roles.html'
        self.context['title'] = 'Roles'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)


    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Roles", "route" : '','active' : True});
        
        
class LoadRolesDatatable(BaseDatatableView):

    model = Role

    order_columns = ['id','name','permissions']
    
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__icontains=search))

        return qs
    

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id' : escape(item.id),
                'encrypt_id': escape(URLEncryptionDecryption.enc(item.id)),
                'name' : escape(item.name),
                'permissions': escape(",".join(str(name) for name in item.permissions.values_list('name', flat=True)))
            })
        return json_data
    
    
     
class RolesCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.context['title'] = 'Roles'
        self.action = "Create"
        self.template = 'admin/user/roles/roles-create-or-update.html'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        
        if id:
            self.context['role'] = get_object_or_404(Role, id=id)
       
        return render(request, self.template , context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Roles", "route" :reverse('users:roles.index') ,'active' : False})
        self.context['breadcrumbs'].append({"name" : "{} Role".format(self.action), "route" : '','active' : True})

    

    def post(self, request, *args, **kwargs):
        role_id = request.POST.get('role_id', None)
        
        try:
            
            permission_ids = request.POST.get('permission_ids', None)
            if permission_ids is not None and permission_ids != '[]':

                permission_ids = json.loads(permission_ids)

                remove_permission_lists = []
                
                if role_id:
                    self.action = 'Updated'
                    
                    role = get_object_or_404(Role, id=role_id)
                    
                    active_permissions_list = Role.objects.get(id=role_id).permissions.all().values_list('id', flat=True)
                    
                    remove_permission_lists = [item for item in active_permissions_list if item not in permission_ids]
                    [permission_ids.remove(item) for item in active_permissions_list if item in permission_ids]
                    
                   
                else:
                    role = Role()
                    self.action = 'Created'
                 
                role.name = request.POST.get('role_name',None)
                role.save()
                
                role_instance = get_object_or_none(Role,id=role.id)
                if role_instance is not None:
                        for permission_id in permission_ids:
                            permission_instance = get_object_or_none(Permission,id=permission_id)
                            if permission_instance is not None:
                                role_instance.permissions.add(permission_instance)
                                    
                        for remove_permission in remove_permission_lists:
                            remove_permission_instance = get_object_or_none(Permission,id=remove_permission)
                            if remove_permission_instance is not None:
                                role_instance.permissions.remove(remove_permission_instance)
                
                
                
                    
                messages.success(request, f"Data Successfully "+ self.action)
            else:

                messages.error(request, "Permissions not applied")
                return redirect('users:roles.create')

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if role_id is not None:
                return redirect('users:roles.update', id=URLEncryptionDecryption.dec(int(role_id)))
            return redirect('users:roles.create')
        
        return redirect('users:roles.index')



@method_decorator(login_required, name='dispatch')
class DestroyRolesView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            role_id = request.POST.getlist('ids[]')
            if role_id:
                Role.objects.filter(id__in=role_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)



class EditRoleView(View):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.action = "update"
        self.template = 'user/permission/roles-edit.html'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        
        id = kwargs.pop('id', None)
        if id:
            self.context['role'] = get_object_or_404(Role, id=id)
            self.context['permission'] = Permission.objects.filter(content_type__model='Custom Content Type')
            
        return render(request, self.template , context=self.context)
       
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Roles", "route" :reverse('users:roles.index') ,'active' : False});
        self.context['breadcrumbs'].append({"name" : "Create Roles", "route" : '','active' : True}) 
    
    def post(self, request, *args, **kwargs):

        role_id = request.POST.get('id', None)
        try:
            if role_id:
                self.action = 'Updated'
                role = get_object_or_404(Role, id=role_id)
            else:
                role = Role()
                self.action = 'Created'

            role.name = request.POST.get('role_name').strip()
            perm=request.POST.getlist('permissions')
            
            for index in perm:
                role.permissions.add(index)
            
            role.save()
            

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            
            if role_id is not None:
                return redirect('users:update-role', id = role_id )   
            return redirect('users:roles.create')

        return redirect('users:roles.index')  


# USER GROUP AND PERMISSION

class GroupView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/user/groups/groups.html'
        self.context['title'] = 'Groups'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template, context=self.context)


    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Groups", "route" : '','active' : True});
        
        
class LoadGroupDatatable(BaseDatatableView):

    model = Group
    
    order_columns = ['id','name','roles']
    
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        
        if search:
            qs = qs.filter(Q(name__icontains=search))

        return qs
    
    def prepare_results(self, qs):
        json_data = []
        for item in qs:

            json_data.append({
                
                'id' : escape(item.id),
                'encrypt_id'    : escape(URLEncryptionDecryption.enc(item.id)), 
                'name' : escape(item.name),
                'role' : escape(",".join(str(name) for name in item.roles.values_list('name', flat=True))),

            })

        return json_data
    
    
@method_decorator(login_required, name='dispatch')
class DestroyGroupView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            group_id = request.POST.getlist('ids[]')
            if group_id:
                Group.objects.filter(id__in=group_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
    
   
class CreateOrUpdateGroupView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.action = "Create"
        self.context = {"breadcrumbs" : []}
        self.context['title'] = 'Groups'
        self.template = 'admin/user/groups/create-or-update-group.html'

    def get(self, request, *args, **kwargs):
        
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update "
            self.context['group'] = get_object_or_404(Group, id=id)
            self.context['active_roles'] = Group.objects.get(id=id).roles.all().values_list('id', flat=True)
            
        self.context['roles'] = Role.objects.filter()
        self.generateBreadcrumbs()
        
        return render(request, self.template, context=self.context)
    
    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False});
        self.context['breadcrumbs'].append({"name" : "Groups", "route" : reverse('users:groups.index') ,'active' : False});
        self.context['breadcrumbs'].append({"name" : "{} group".format(self.action), "route" : '','active' : True});

    def post(self, request, *args, **kwargs):
        group_id = request.POST.get('group_id', None)
        try:
            
            roles = request.POST.getlist('role')
            remove_roles_lists = []
        
            if group_id:
                
                self.action = 'Updated'
                group = get_object_or_404(Group, id=group_id)
                
                active_roles_list = Group.objects.get(id=group_id).roles.all().values_list('id', flat=True)
                
                remove_roles_lists = [item for item in active_roles_list if str(item) not in roles]
                [roles.remove(str(item)) for item in active_roles_list if str(item) in roles]
            
            else:
                group = Group()
                self.action = 'Created'

                
            group.name = request.POST.get('group_name',None)
            group.save()
            group_instance = get_object_or_none(Group,id=group.id)
            
            
            if group_instance is not None:
                for role in roles:
                    role_instance = get_object_or_none(Role, id=role)
                    group_instance.roles.add(role_instance)
                    
                for remove_role in remove_roles_lists:
                    remove_role_instance = get_object_or_none(Role, id=remove_role)
                    if remove_role_instance is not None:
                        group_instance.roles.remove(remove_role_instance)
            
            messages.success(request, f"Data Successfully "+ self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if group_id is not None:
                return redirect('users:group.update', id=URLEncryptionDecryption.enc(int(group_id)))
            return redirect('users:group.create')
        return redirect('users:groups.index')








class GeneratePermissionInTreeView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}
        
    def post(self, request, *args, **kwargs):
        try:
            
            role_id = request.POST.get('role_id','')
            permissions = Permission.objects.all()
            
            serializer = PermissionSerializer(permissions, many=True, context={"request": request})
            
            
            initial_app_label_lists = []
            
            for permission in serializer.data:
                
                label_text = "{}".format(permission.get('label').capitalize().strip())
                
                initial_app_label_lists.append({
                    "text": label_text,
                })
                
                
            initial_app_label_lists = [dict(t) for t in {tuple(d.items()) for d in initial_app_label_lists}]
            
            
            
            for permission in serializer.data:
                role_permission_exists = False
                permission_id = permission.get('id')
                if role_id is not None and role_id != '':
                    role_permission_exists = Role.objects.filter(Q(permissions__in=[permission_id]) & Q(id=role_id)).exists()
            
                label_text = "{}".format(permission.get('label').capitalize().strip())
                
                for key , initial_app_label_list in enumerate(initial_app_label_lists):
                    
                    if str(label_text) == str(initial_app_label_list.get('text')):
                        
                        if not 'children' in initial_app_label_lists[key].keys():
                            
                            initial_app_label_lists[key]['children'] = list()
                        
                        initial_app_label_lists[key]['children'].append({
                            'text' : permission.get('name'),
                            'li_attr': { "permission_id": permission_id },
                            'a_attr': { "permission_id": permission_id },
                            "state": {
                                "selected": True if role_permission_exists else False
                            },
                            "icon" : "fa-solid fa-key custom-secondary-color fs-4" 
                        })

            
            self.response_format['status_code'] = 200
            self.response_format['data'] = initial_app_label_lists
            
            
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)
    
    
"""-------------------------VCustomer Users Users Listing---------------------"""

class CustomerView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs" : []}
        self.template = 'admin/customers-listing/customers-listing-listing.html'  
        self.context['title'] = 'Customer'
        self.generateBreadcrumbs()
        
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name" : "Home", "route" : reverse('home:dashboard'),'active' : False})
        self.context['breadcrumbs'].append({"name" : "Customer", "route" : '','active' : True})


class LoadCustomerDatatable(BaseDatatableView):
    model = Users
    order_columns = ['id','full_name','email','phone'] 
    
    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return Users.objects.filter(Q(is_admin=False)& Q(is_staff=False)& Q(is_superuser=False)).order_by('-id')
    
    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(email__istartswith=search)|Q(full_name__istartswith=search)|Q(phone__istartswith=search))
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id'              : escape(item.id),
                'email'           : escape(item.email),
                'name'            : escape(item.full_name),
                'mobile_number'   : escape(item.phone),
                # 'encrypt_id'      : escape(URLEncryptionDecryption.enc(item.id)),
            })
        return json_data


# @method_decorator(login_required, name='dispatch')
# class DestroySellYouCarEnquiryEnquieryRecordsView(View):
#     def __init__(self, **kwargs):
#         self.response_format = {"status_code": 101, "message": "", "error": ""}

#     def post(self, request, *args, **kwargs):
#         try:
#             instance_id = request.POST.getlist('ids[]')
#             if instance_id:
#                 SellYouCarEnquiry.objects.filter(id__in=instance_id).delete()
#                 self.response_format['status_code'] = 200
#                 self.response_format['message'] = 'Success'
#         except Exception as e:
#             self.response_format['message'] = 'error'
#             self.response_format['error'] = str(e)
#         return JsonResponse(self.response_format, status=200)


# class SellYouCarEnquiryEnquiryContactedStatusChange(View):
#     def __init__(self, **kwargs):
#         self.response_format = {"status_code":101, "message":"", "error":""}
        
#     def post(self, request, **kwargs):
#         try:
#             instance_id = request.POST.get('id', None)
#             instance = SellYouCarEnquiry.objects.get(id = instance_id)
#             if instance_id:
#                 if instance.is_contacted:
#                     instance.is_contacted = False
#                 else:
#                     instance.is_contacted =True
#                 instance.save()
#                 self.response_format['status_code']=200
#                 self.response_format['message']= 'Success'
                
#         except Exception as es:
#             self.response_format['message']='error'
#             self.response_format['error'] = str(es)
#         return JsonResponse(self.response_format, status=200)



# class SellYouCarEnquiryEnquieryDetailViewView(View):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.context = {"breadcrumbs": [],}
#         self.action = "Create"
#         self.context['title'] = 'Selling Enquiry'
#         self.template = 'admin/home-page/contact-us/selling-enquiry/selling-enquiry-detail.html'

#     def get(self, request, *args, **kwargs):
#         id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
#         if id:
#             self.action = "Detail View"
#             self.context['instance'] = get_object_or_404(SellYouCarEnquiry, id=id)
#             car_images = CarMultipleImage.objects.filter(car_id=id)
#             if car_images :
#                 self.context['car_images'] = CarMultipleImage.objects.filter(car_id=id)
#             else:
#                 self.context['car_images'] = None
            
#         self.generateBreadcrumbs()
#         return render(request, self.template, context=self.context)

#     def generateBreadcrumbs(self):
#         self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
#         self.context['breadcrumbs'].append({"name": "Selling Enquiry", "route": reverse('contact:Booking_enquiry.view.index'), 'active': False})
#         self.context['breadcrumbs'].append({"name": "{}".format(self.action), "route": '', 'active': True})