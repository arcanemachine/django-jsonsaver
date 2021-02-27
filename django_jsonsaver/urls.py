from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # project_folder
    path('', views.project_root, name='project_root'),
    path('contact_us', views.ContactUsFormView.as_view(), name='contact_us'),
    path('api/', views.project_root_api, name='project_root_api'),

    # local apps
    path('stores/', include('stores.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),

    # third-party apps
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
    path('api/v1/', include('api.urls')),
    path('api/api-token-auth/', obtain_auth_token, name='obtain_auth_token'),
    path('api-auth/', include('rest_framework.urls')),
    path('captcha/', include('captcha.urls')),

    # experimental/debug
    # path('send-test-email/', views.test_email, name='test_email'),
]
