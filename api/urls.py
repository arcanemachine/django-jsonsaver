from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register('stores', views.JsonStoreViewSet, basename='jsonstore')

urlpatterns = [
    path('',
         views.api_root,
         name='api_root'),
    path('stores/all/',
         views.JsonStoreListAll.as_view(),
         name='jsonstore_list_all'),
    path('stores/name/<str:jsonstore_name>/',
         views.JsonStoreDetailName.as_view(),
         name='jsonstore_detail_name'),
    path('stores/public/<str:jsonstore_name>/',
         views.JsonStoreDetailPublic.as_view(),
         name='jsonstore_detail_public'),
] + router.urls
