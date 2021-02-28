from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('',
         views.ProjectRootTemplateView.as_view(),
         name='project_root'),
    path('contact-us/',
         views.ContactUsFormView.as_view(),
         name='contact_us'),
    path('terms-of-use/',
         views.TermsOfUseTemplateView.as_view(),
         name='terms_of_use'),
    path('privacy-policy/',
         views.PrivacyPolicyTemplateView.as_view(),
         name='privacy_policy'),

    # local
    path('admin/', admin.site.urls),
    path('api/', include('api_generic.urls')),
    path('api/v1/', include('api.urls')),
    path('store/', include('stores.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),

    # third-party
    path('captcha/', include('captcha.urls')),
]
