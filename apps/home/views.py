import json
import logging
import uuid
from apps.home.functions import ConvertBase64File
from todo import settings
from todo.helpers.module_helper import imageDeletion
from django.contrib import messages
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.urls import reverse
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from todo.helpers.signer import URLEncryptionDecryption
import requests
from urllib.parse import urlparse
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
logger = logging.getLogger(__name__)
from apps.users.models import Users
from apps.project.models import Project

class HomeView(View):
    def __init__(self):
        self.context = {}
        self.context['title'] = 'Dashboard'

    def get(self, request, *args, **kwargs):
        
        project_count = Project.objects.all()
        if project_count:
            self.context['total_project'] = project_count.count()
        else:
            self.context['total_project'] = '0'

        
        return render(request, "admin/home/dashboard.html", self.context)

