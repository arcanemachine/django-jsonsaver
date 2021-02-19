from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('', views.project_root, name='project_root'),
    path('admin/', admin.site.urls),
]
