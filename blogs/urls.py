from django.urls import path
from . import views

app_name='blogs'
urlpatterns = [
    path('', views.application, name='application'),
    path('index', views.index, name='index'),
    path('posts/<str:tag>/', views.tagSearch, name='tagSearch'),
    path('<str:username>/notebox/index', views.noteBox, name='noteBox'),
    path('<str:username>/notebox/index/new', views.noteNew, name='noteNew'),
    path('<str:username>/notebox/delete/<int:pk>', views.noteDelete, name='noteDelete')
]
