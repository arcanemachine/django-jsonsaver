from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import include, path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # django_jsonsaver
    path('', views.project_root, name='project_root'),
    path('contact_us', views.ContactUsFormView.as_view(), name='contact_us'),

    # local apps
    path('stores/', include('stores.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),

    # third-party apps
    path('api/', views.project_root_api, name='project_root_api'),
    path('api/v1/', include('api.urls')),
    path('api/api-token-auth/', obtain_auth_token, name='obtain_auth_token'),
    path('api-auth/', include('rest_framework.urls')),
    path('captcha/', include('captcha.urls')),

    # experimental/debug
    # path('send-test-email/', views.test_email, name='test_email'),
]
