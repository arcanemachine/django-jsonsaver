from django.urls import path

from . import views

app_name = 'jsonsaver'

urlpatterns = [
    path('',
         views.JsonStoreListView.as_view(),
         name='jsonstore_list'),

    # create
    path('new/',
         views.JsonStoreCreateView.as_view(),
         name='jsonstore_create'),

    # detail
    path('<int:jsonstore_pk>/',
         views.JsonStoreDetailView.as_view(),
         name='jsonstore_detail'),
    path('name/<str:jsonstore_name>/',
         views.JsonStoreNameDetailView.as_view(),
         name='jsonstore_detail_name'),
    path('public/<str:jsonstore_name>/',
         views.JsonStorePublicNameDetailView.as_view(),
         name='jsonstore_detail_public'),

    # update
    path('<int:jsonstore_pk>/update/',
         views.JsonStoreUpdateView.as_view(),
         name='jsonstore_update'),

    # delete
    path('<int:jsonstore_pk>/delete/',
         views.JsonStoreDeleteView.as_view(),
         name='jsonstore_delete'),

]
