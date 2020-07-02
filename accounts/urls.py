from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
  path('signin', views.signin, name='signin'),
  path('signup', views.signup, name='signup'),
  path('signout', views.logout, name='signout'),
  path('update', views.update, name='update'),
  path('profile', views.profile, name='profile'),
  path('update/secession', views.secession, name='secession'),
  path('signfind', views.signfind, name='signfind'),
  path('signfound', views.signfound, name='signfound'),
  path('<str:username>/following', views.following, name='following'),
  path('<str:username>/like', views.blogLike, name='blogLike'),
]
