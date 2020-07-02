from django.shortcuts import render

from accounts.models import User
from accounts.models import Profile
from posts.models import Posts

from django.db.models import Q

# Create your views here.
def searchResult(request):
  posts = None

  user_id = request.session.get('user_id')

  if user_id:
    if 'q' in request.GET:
      query = request.GET.get('q')

      user = User.objects.get(pk=user_id)
      profile = Profile.objects.get(user_id=user_id)
      posts = Posts.objects.all().filter(Q(contents__contains=query) | Q(title__contains=query))

      context = {'query': query, 'bloger': user, 'profile': profile, 'posts': posts}
      
      if len(posts) == 0:
        context['message'] = "검색어가 포함된 포스트가 없습니다."

    return render(request, 'search/index.html', context)

def myBlogSearchResult(request, username):
  posts = None

  user_id = request.session.get('user_id')

  if user_id:
    if 'mq' in request.GET:
      query = request.GET.get('mq')

      user = User.objects.get(pk=user_id)
      profile = Profile.objects.get(user_id=user_id)
      posts = Posts.objects.filter(Q(contents__contains=query) | Q(title__contains=query), user_id=user_id)

      context = {'query': query, 'bloger': user, 'profile': profile, 'posts': posts}

      if len(posts) == 0:
        context['message'] = "검색어가 포함된 포스트가 없습니다."

    return render(request, 'search/index.html', context)