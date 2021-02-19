from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register('json', views.JsonStoreViewSet)

urlpatterns = router.urls + [
    path('', views.JsonStoreList.as_view(), name='jsonstore_list'),
]
