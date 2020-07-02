from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('<str:username>/', views.posts, name="posts"),
    path('<str:username>/new', views.new, name='new'),
    path('<str:username>/sortPosts/<int:ct>/', views.sortPosts, name="sortPosts"),
    path('<str:username>/post/<int:ct>/<int:pk>/', views.detail, name='detail'),
    path('<str:username>/post/<int:ct>/<int:pk>/edit', views.edit, name='edit'),
    path('<str:username>/post/<int:ct>/<int:pk>/delete', views.delete, name='delete'),
    path('<str:username>/post/<int:ct>/<int:pk>/like', views.like, name='like'),
    path('posts/note', views.note, name='note'),
    path('posts/mail', views.mail, name='mail')
]
