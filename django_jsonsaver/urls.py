from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('', views.ProjectRootTemplateView.as_view(), name='project_root'),
    path('contact_us/', views.ContactUsFormView.as_view(), name='contact_us'),
    path('terms-of-use/',
         views.TermsOfUseTemplateView.as_view(),
         name='terms_of_use'),
    path('privacy-policy/',
         views.PrivacyPolicyTemplateView.as_view(),
         name='privacy_policy'),

    # local apps
    path('admin/', admin.site.urls),
    path('store/', include('stores.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),

    # third-party apps
    path('api/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='api_schema'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/', include('api.urls')),
    path('api/api-token-auth/', obtain_auth_token, name='obtain_auth_token'),
    path('api-auth/', include('rest_framework.urls')),
    path('captcha/', include('captcha.urls')),
]
