from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register('json', views.JsonStoreViewSet)

urlpatterns = router.urls + [
    path('',
         views.api_root,
         name='api_root'),
    path('json/ref/',
         views.ref_root,
         name='ref_root'),
    path('json/ref/<str:ref>/',
         views.JsonStoreRefDetail.as_view(),
         name='ref_detail')
]
