from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('',
         views.users_root,
         name='users_root'),
    path('register/',
         views.UserRegisterView.as_view(),
         name='register'),
    path('confirm/<str:confirmation_code>/',
         views.user_confirm,
         name="user_confirm"),
    path('login/',
         views.UserLoginView.as_view(),
         name='login'),
    path('me/',
         views.UserDetailView.as_view(),
         name='user_detail'),
    path('logout/',
         views.UserLogoutView.as_view(),
         name='logout'),
]
