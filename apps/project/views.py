from django.shortcuts import render, get_object_or_404, redirect
import logging
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views import View
from django.urls import reverse
from django.utils.html import escape
from django.http import JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import *
from todo.helpers.signer import URLEncryptionDecryption
from apps.project.models import Project, Todo

logger = logging.getLogger(__name__)

#Create or update Project 
class ProjectCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": [], }
        self.action = "Create"
        self.context['categories_title'] = 'Project'
        self.template = 'admin/home-page/project/create-or-update-project.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Project, id=id)

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})

        self.context['breadcrumbs'].append({"name": "{} Project".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Project, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Project()
                self.action = 'Created'

            instance.title = request.POST.get('title', None)
            instance.created_by = request.user
            instance.save()

            messages.success(request, f"Data Successfully " + self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            if instance_id is not None and instance_id != '':
                return redirect('project:project.update', id=URLEncryptionDecryption.dec(int(instance_id)))
            return redirect('project:project.create')
        return redirect('project:project.index')

#Listing of Projects
 
class ProjectView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.template = 'admin/home-page/project/list-projects.html'
        self.context['title'] = 'Projects'
        self.generateBreadcrumbs()

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        self.context['categories'] = projects
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Project", "route": '', 'active': True})

    
class LoadProjectsDatatable(BaseDatatableView):
    model = Project
    order_columns = ['id', 'title']

    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return Project.objects.all().order_by('-id')

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(title__istartswith=search)
            )
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id': escape(item.id),
                'title': escape(item.title),
                'created_date': escape(item.created_date.strftime('%d/%m/%Y') if item.created_date else ''),
                'modified_date': escape(item.modified_date.strftime('%d/%m/%Y') if item.modified_date else ''),
                'is_active': escape(item.is_active),
                'encrypt_id': escape(URLEncryptionDecryption.enc(item.id))
            })
        return json_data
    
#Status change of Projects
class ProjectStatusChange(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Project.objects.get(id = instance_id)
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
    
#Deleting Projects

class DestroyProjectRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Project.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)

class ProjectDetailViewView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.action = "Create"
        self.context['title'] = 'Project'
        self.template = 'admin/home-page/project/projectdetailed.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Detailed View"
            instance = get_object_or_404(Project, id=id)
            todos = Todo.objects.filter(project=instance)
            self.context['instance'] = instance
            self.context['todos'] = todos

        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Project", "route": reverse('project:project.index'), 'active': False})
        self.context['breadcrumbs'].append({"name": "{}".format(self.action), "route": '', 'active': True})
    
#_____________________________________TODO______________________________________________________________________
    

class TodoView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": []}
        self.template = 'admin/home-page/todo/list_todo.html'
        self.context['categories_title'] = 'Todo'
        self.generateBreadcrumbs()

    def get(self, request, *args, **kwargs):
        categories = Todo.objects.all()
        self.context['categories'] = categories
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})
        self.context['breadcrumbs'].append({"name": "Todo", "route": '', 'active': True})

    
class LoadTodoDatatable(BaseDatatableView):
    model = Todo
    order_columns = ['id']

    def get_initial_queryset(self):
        filter_value = self.request.POST.get('columns[3][search][value]', None)
        if filter_value == '1':
            return self.model.objects.filter(is_active=True).order_by('-id')
        elif filter_value == '2':
            return self.model.objects.filter(is_active=False).order_by('-id')
        else:
            return Todo.objects.all().order_by('-id')

    def filter_queryset(self, qs):
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(todo_title__istartswith=search)

            )
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id': escape(item.id),
                'todo_title':escape(item.todo_title),
                'project': escape(item.project.title),  
                'created_date': escape(item.created_date.strftime('%d/%m/%Y') if item.created_date else ''),
                'modified_date': escape(item.modified_date.strftime('%d/%m/%Y') if item.modified_date else ''),  
                'description':escape(item.description),
                'status': escape(item.status),
                # 'is_active':escape(item.is_active),
                'encrypt_id': escape(URLEncryptionDecryption.enc(item.id))
            })
        return json_data
    

class ActiveInactiveTodo(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code":101, "message":"", "error":""}
        
    def post(self, request, **kwargs):
        try:
            instance_id = request.POST.get('id', None)
            instance = Todo.objects.get(id = instance_id)
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


class TodoCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {"breadcrumbs": [], }
        self.action = "Create"
        self.context['categories_title'] = 'Subcategories'
        self.template = 'admin/home-page/todo/create-or-update-todo.html'

    def get(self, request, *args, **kwargs):
        id = URLEncryptionDecryption.dec(kwargs.pop('id', None))
        if id:
            self.action = "Update"
            self.context['instance'] = get_object_or_404(Todo, id=id)

        self.context['todo_choices'] = Todo.STATUS_CHOICES
        self.context['projects'] = Project.objects.filter(is_active=True)
        self.generateBreadcrumbs()
        return render(request, self.template, context=self.context)

    def generateBreadcrumbs(self):
        self.context['breadcrumbs'].append({"name": "Home", "route": reverse('home:dashboard'), 'active': False})

        self.context['breadcrumbs'].append({"name": "{} TODO".format(self.action), "route": '', 'active': True})

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id', None)
        try:
            if instance_id:
                self.action = 'Updated'
                instance = get_object_or_404(Todo, id=instance_id)
                instance.updated_by = request.user
            else:
                instance = Todo()
                self.action = 'Created'

            instance.todo_title   = request.POST.get('todo_title', None)
            instance.description    = request.POST.get('todo_description', None)
            instance.status         = request.POST.get('status', None)
            project_id              = request.POST.get('project', None)
            if project_id:
                instance.project = get_object_or_404(Project, id=project_id)
            instance.created_by   = request.user
            instance.save()

            messages.success(request, f"Data Successfully " + self.action)
        except Exception as e:
            messages.error(request, f"Something went wrong." + str(e))
            if instance_id is not None and instance_id != '':
                return redirect('project:todo.update', id=URLEncryptionDecryption.dec(int(instance_id)))
            return redirect('project:todo.create')
        return redirect('project:todo-view.index')



@method_decorator(login_required, name='dispatch')
class DestroyTodoRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            instance_id = request.POST.getlist('ids[]')
            if instance_id:
                Todo.objects.filter(id__in=instance_id).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
        return JsonResponse(self.response_format, status=200)


#Check duplication of projects

class CheckProjectView(View):
    
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data": []}

    def post(self, request, *args, **kwargs):
        try:
            category_name = request.POST.get('category_name', None)
            
            if category_name:
                exists = Project.objects.filter(title=category_name).exists()
                
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
                self.response_format['data'] = {'exists': exists}

        except Exception as e:
            self.response_format['message'] = 'Error'
            self.response_format['error'] = str(e)

        return JsonResponse(self.response_format, status=self.response_format['status_code'])
    
#Check Todo already exist or not

class CheckTodoView(View):
    
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": "", "data": []}

    def post(self, request, *args, **kwargs):
        try:
            category_name = request.POST.get('category_name', None)
            
            if category_name:
                exists = Todo.objects.filter(todo_title=category_name).exists()
                
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
                self.response_format['data'] = {'exists': exists}

        except Exception as e:
            self.response_format['message'] = 'Error'
            self.response_format['error'] = str(e)

        return JsonResponse(self.response_format, status=self.response_format['status_code'])
