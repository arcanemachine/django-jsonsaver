from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register('json', views.JsonStoreViewSet)

urlpatterns = [
    path('',
         views.api_root,
         name='api_root'),
    path('json/all/',
         views.JsonStoreListAll.as_view(),
         name='jsonstore_list_all'),
    path('json/name/',
         views.name_root,
         name='name_root'),
    path('json/name/<str:name>/',
         views.JsonStoreNameDetail.as_view(),
         name='name_detail'),
] + router.urls
