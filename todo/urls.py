from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve
from todo.views import page_not_found_view, custom_500

admin.site.site_header = "TODO"
admin.site.site_title = "TODO"

schema_view = get_schema_view(
   openapi.Info(
      title="TODO",
      default_version='v1',
      terms_of_service="",
      contact=openapi.Contact(email="musthakpt786@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    path('', include('apps.home.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('admins/', include('apps.admins.urls')),
    path('admins/', include('apps.project.urls')),
    
    
    
    re_path(r'^api/', include([
        
        path('auth/', include('apps.authentication.api.urls')),
        path('users/', include('apps.users.api.urls')),
        path('home/', include('apps.home.api.urls')),

    
        re_path(r'^docs/', include([

            path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path("redoc", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        ])),    
    ])),    
    
        
    
] 


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found_view
handler500 = custom_500
