import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from apps.users.models import Users
from django.contrib import messages


logger = logging.getLogger(__name__)


class LoginView(View):

    def __init__(self):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:dashboard')
        return render(request, 'admin/auth/login.html')

    def post(self, request, *args, **kwargs):
    
        try:
            
            email    = request.POST.get('email')
            password = request.POST.get('password')
            user     = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                self.response_format['status_code'] = 100
                self.response_format['message'] = f"Success"
            else:
                self.response_format['message'] = 'Invalid username or password'
            messages.success(request, f"Login Successfully Completed")
        except Exception as e:
            self.response_format['message'] = 'Something went wrong, Please try again later.'
            self.response_format['error'] = str(e)

        return JsonResponse(self.response_format, status=200)



def signout(request):
    logout(request)
    return redirect('authentication:login')



