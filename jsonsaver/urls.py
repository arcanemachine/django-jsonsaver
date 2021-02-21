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
    path('<int:jsonstore_pk>/',
         views.JsonStoreDetailView.as_view(),
         name='jsonstore_detail'),
    path('<str:jsonstore_name>/',
         views.JsonStoreNameDetailView.as_view(),
         name='jsonstore_detail'),
    path('public/<str:jsonstore_name>/',
         views.JsonStorePublicNameDetailView.as_view(),
         name='jsonstore_detail'),
]
