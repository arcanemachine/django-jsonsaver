from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register('json', views.JsonItemViewSet)

urlpatterns = router.urls + [
    path('', views.JsonItemList.as_view(), name='jsonitem_list'),
]
