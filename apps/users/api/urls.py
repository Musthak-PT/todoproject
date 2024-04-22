from django.urls import path, include,re_path
from django.contrib import admin
from . import views


urlpatterns = [       
   re_path(r'^register/', include([
      path('customer-profile-registration',views.CreateOrUpdateUserProfileManagement.as_view()),
   ])),
   re_path(r'^profile/', include([
      path('get-my-profile',views.GetMyProfileListingApiView.as_view()),
      path('change-password', views.ChangePasswordApiView.as_view()),
    ])),
]

