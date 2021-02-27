from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register('store', views.JsonStoreViewSet, basename='jsonstore')

urlpatterns = [
    path('',
         views.api_root,
         name='api_root'),
    # path('store/all/',
    #      views.JsonStoreListAll.as_view(),
    #      name='jsonstore_list_all'),
    path('store/name/<str:jsonstore_name>/',
         views.JsonStoreDetailName.as_view(),
         name='jsonstore_detail_name'),
    path('store/public/<str:jsonstore_name>/',
         views.JsonStoreDetailPublic.as_view(),
         name='jsonstore_detail_public'),
] + router.urls
