from django.urls import include, path, re_path
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers

urlpatterns = [       
   re_path(r'^web/', include([
      path('final-registration', views.FinalRegistrationAPIView.as_view()),
      path('login', views.LoginAPIView.as_view()),
      path('logout', views.LogoutAPIView.as_view()),
      path('refresh-token', views.RefreshTokenView.as_view()),

      path('customer-register', views.CreateOrUpdateCustomerRegistrationApiView.as_view()),
      path('get-all-customers', views.GetAllCustomerApiView.as_view()),
      path('update-customer-profile', views.UpdateProfileCustomerApiView.as_view()),
      path('get-customer-profile', views.GetProfileCustomerApiView.as_view()),

      path('update-profile-picture', views.UpdateProfilePictureCustomerApiView.as_view()),
      path('get-profile-picture', views.GetProfilePictureApiView.as_view()),

      path('customer-login',views.CustomerLoginView.as_view()),
      path('change-password', views.ChangePasswordApiView.as_view()),

      
      path('forgot-password', views.UserAdminForgotPasswordAPIView.as_view()),
      path('reset-password', views.AdminPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   ])),
]

