from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api_generic'

urlpatterns = [
    # schema
    path('',
         SpectacularRedocView.as_view(
             url_name='api_generic:schema_yml'),
         name='schema'),
    path('schema.yml',
         SpectacularAPIView.as_view(),
         name='schema_yml'),

    # local
    path('v1/', include('api.urls')),

    # third-party
    path('auth/', include('rest_framework.urls')),
    path('auth/obtain-auth-token/',
         obtain_auth_token,
         name='obtain_auth_token'),
]
