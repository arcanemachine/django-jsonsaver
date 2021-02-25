from django.urls import path

from . import views

app_name = 'jsonsaver'

urlpatterns = [
    path('find/',
         views.JsonStoreLookupPublicView.as_view(),
         name='jsonstore_lookup_public'),
    path('',
         views.JsonStoreListView.as_view(),
         name='jsonstore_list'),
    path('new/',
         views.JsonStoreCreateView.as_view(),
         name='jsonstore_create'),

    path('<int:jsonstore_pk>/',
         views.JsonStoreDetailView.as_view(),
         name='jsonstore_detail'),
    path('name/<str:jsonstore_name>/',
         views.JsonStoreNameDetailView.as_view(),
         name='jsonstore_detail_name'),
    path('public/<str:jsonstore_name>/',
         views.JsonStorePublicNameDetailView.as_view(),
         name='jsonstore_detail_public'),

    path('<int:jsonstore_pk>/update/',
         views.JsonStoreUpdateView.as_view(),
         name='jsonstore_update'),
    path('<int:jsonstore_pk>/delete/',
         views.JsonStoreDeleteView.as_view(),
         name='jsonstore_delete'),
]
