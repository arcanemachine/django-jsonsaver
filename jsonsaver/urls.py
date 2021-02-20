from django.urls import path

from . import views

app_name = 'jsonsaver'

urlpatterns = [
    path('',
         views.jsonsaver_root,
         name='jsonsaver_root'),
    path('new/',
         views.JsonStoreCreateView.as_view(),
         name='jsonstore_create'),
    path('<str:store_name>/',
         views.JsonStoreDetailView.as_view(),
         name='jsonstore_detail'),
]
