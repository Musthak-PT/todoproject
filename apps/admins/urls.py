from django.urls import include, path, re_path

from apps.admins.views import *

app_name = 'admins'

urlpatterns = [
    re_path(r'^admins-users/', include([
        path('', login_required(AdminsView.as_view()), name='admins.index'),
        path('create', login_required(AdminCreateOrUpdateView.as_view()), name='admins.create'),
        path('<str:id>/update/', login_required(AdminCreateOrUpdateView.as_view()), name='admins.update'),
        path('load-admins-datatable', login_required(LoadAdminsDatatable.as_view()), name='load.admins.datatable'),
        path('destroy-records/', login_required(DestroyAdminsRecordsView.as_view()), name='admins.records.destroy'),
        path('check-email/',login_required(CheckEmailExistRecordsView.as_view()),name='admin.email_exist_check'),
        path('check-mobile/', login_required(CheckMobileExistRecordsView.as_view()), name='admin.mobile_exist_check'), 
        path('active-inactive-admin/', login_required(ActiveInactiveAdminStatus.as_view()), name="active.or.inactive.admins_status"),       
        ])),
    
    re_path(r'^password/', include([
        path('change-password/',login_required(AdminChangePasswordView.as_view()),name='admin.change-password'),
        path('forgot-password/',AdminForgotPasswordPasswordView.as_view(),name='admin.forgot_password'),
        path('rest-password/<uidb64>/<token>/',AdminResetPasswordView.as_view(),name='admin.reset_password'),
        path('rest-password/',AdminResetPasswordView.as_view(),name='admin.reset_change_password'),
        
        ])),
]
