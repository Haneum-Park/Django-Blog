from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('result', views.searchResult, name='searchResult'),
    path('result/<str:username>/',views.myBlogSearchResult, name='myBlogSearchResult')
]
