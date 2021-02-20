from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # local apps
    path('', views.project_root, name='project_root'),
    # path('email-me/', views.test_email, name='test_email'),
    path('stores/', include('jsonsaver.urls')),
    path('users/', include('users.urls')),

    # third-party apps
    path('api/v1/', include('api.urls')),
    path('api/api-token-auth/', obtain_auth_token, name='obtain_auth_token'),
    path('api-auth/', include('rest_framework.urls')),
    path('captcha/', include('captcha.urls')),

]
