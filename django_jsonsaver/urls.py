from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.project_root, name='project_root'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
