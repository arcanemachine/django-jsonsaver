from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register('jsonstore', views.JsonStoreViewSet, basename='jsonstore')

urlpatterns = [
    path('',
         views.api_root,
         name='api_root'),
    path('jsonstore/name/<str:jsonstore_name>/',
         views.JsonStoreDetailName.as_view(),
         name='jsonstore_detail_name'),
    path('jsonstore/public/<str:jsonstore_name>/',
         views.JsonStoreDetailPublic.as_view(),
         name='jsonstore_detail_public'),
] + router.urls
