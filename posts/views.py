import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import Http404
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from django.urls import reverse

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.conf import settings

from .models import Posts
from .models import Comments
from .models import Categories
from .models import Note
from .models import Mail

from accounts.models import User
from accounts.models import Profile

# Create your views here.
def posts(request, username):
  user_id = request.session.get('user_id')

  if user_id:
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    categories = Categories.objects.all()
    note = Note.objects.filter(to_user_id=user.username)
    mail = Mail.objects.filter(mail_to_user_id=user.username)

    context = {'bloger': user, 'profile': profile,
               'categories': categories, 'note': note, 'mail': mail}

    blog_author = User.objects.get(username=username)
    blog_author_profile = Profile.objects.get(username=username)

    if user.username != blog_author.username:
      context['blog_author'] = blog_author
      context['blog_author_profile'] = blog_author_profile

    post_all = Posts.objects.filter(author_id=username)  # 특정 조건에 맞는 열 가져오기

    pagniator = Paginator(post_all, 10)  # 보여지는 모델, 보일 개수

    page = request.GET.get('page')

    posts = pagniator.get_page(page)

    if len(posts) == 0:
      context['message'] = "게시된 포스트가 없습니다."
    else:
      context['posts'] = posts
    return render(request, 'posts/index.html', context)

  else:
    return redirect('/signin')


def sortPosts(request, username, ct):
  user_id = request.session.get('user_id')

  if user_id:
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    categories = Categories.objects.all()
    current_categories = Categories.objects.get(value=ct)

    blog_author = User.objects.get(username=username)
    blog_author_profile = Profile.objects.get(username=username)

    context = {
      'bloger': user, 
      'profile': profile, 
      'categories': categories, 
      'current_categories': current_categories,
    }

    if user.username != blog_author.username:
      context['blog_author'] = blog_author
      context['blog_author_profile'] = blog_author_profile

    posts = Posts.objects.filter(author_id=username, category_id=ct)  # 특정 조건에 맞는 열 가져오기

    if len(posts) == 0:
      context['message'] = "현재 " + current_categories.name + "에 게시된 포스트가 없습니다."
    else:
      context['posts'] = posts
    return render(request, 'posts/index.html', context)
  
  else:
    return redirect('/signin')


def new(request, username):
  response_data = {}

  user_id = request.session.get('user_id')
  if user_id:
    user = User.objects.get(pk=user_id)
    categories = Categories.objects.all()

    if request.method == "GET":
      return render(request, 'edit/new.html', {
        'bloger': user,
        'categories': categories
      })

    elif request.method == "POST":
      title = request.POST.get('title', None)
      contents = request.POST.get('contents', None)
      category_id = request.POST.get('category', None) # 카테고리의 id가 아닌 value를 가져옴
      tags = request.POST.get('tags', None)

      if not title and contents and category_id:
        response_data['error'] = "입력하지 않은 항목이 있습니다."
      else:
        posts = Posts(user_id=user.id, author_id=username, title=title, contents=contents, tags=tags, category_id=category_id)
        posts.save()
        return redirect('/' + username + '/')
  else:
    return redirect('/index')


def detail(request, username, ct, pk):
  user_id = request.session.get('user_id')
  if user_id:
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    post = Posts.objects.get(pk=pk)
    note = Note.objects.filter(id=user.id)
    mail = Mail.objects.filter(id=user.id)

    post_tags = post.tags
    post_tags = post_tags.split(',')

    context = {'bloger': user, 'profile': profile, 'post': post, 'note': note, 'mail': mail, 'post_tags': post_tags}

    blog_author = User.objects.get(username=username)
    blog_author_profile = Profile.objects.get(username=username)

    if user.username != blog_author.username:
      context['blog_author'] = blog_author
      context['blog_author_profile'] = blog_author_profile

    try:
      comments = Comments.objects.filter(post_id=pk)
      context['comments'] = comments
    except:
      print("댓글이 없습니다.")

    if request.method == "GET":
      post.views += 1
      post.save()

      return render(request, 'posts/detail.html', context)

    elif request.method == "POST":
      comment_in_comment = request.POST.get('comment_in_comment')
      comment_id = request.POST.get('comment_id')
      comment = request.POST.get('comment')

      if comment:
          comments_create = Comments(user_id=user.id, post_id=pk, name=user.name, username_id=user.username, comment=comment)
          comments_create.save()
      elif comment_in_comment:
          comments_create = Comments(user_id=user.id, post_id=pk, parent_id=comment_id,name=user.name, username_id=user.username, comment=comment_in_comment)
          comments_create.save()
      return redirect('/' + username + '/post/' + str(ct) + '/' + str(pk))
  else:
    return redirect('/signin')


def edit(request, username, ct, pk):
  user_id = request.session.get('user_id')

  if user_id:
    user = User.objects.get(pk=user_id)
    post = Posts.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=user_id)
    categories = Categories.objects.all()

    context = {
      'bloger': user,
      'profile': profile,
      'post': post,
      'categories': categories
    }

    if request.method == "GET":
      current_category = Categories.objects.get(value=ct)
      context['current_category_value'] = current_category.value
      context['current_category_name'] = current_category.name

      return render(request, 'edit/edit.html', context)
    elif request.method == "POST":
      title = request.POST.get('title')
      contents = request.POST.get('contents')
      category = request.POST.get('category')
      tags = request.POST.get('tags')

      post.title = title
      post.contents = contents
      post.category_id = category
      post.tags = tags
      post.save()
      
      return redirect('/' + username + '/post/' + str(ct) + '/' + str(pk))
  else:
    return redirect('/index')


def delete(request, username, ct, pk):
  post = Posts.objects.get(pk=pk)
  post.delete()
  return redirect(username + '/')


def like(request, username, pk, ct):
  user_id = request.session.get('user_id')

  if user_id:
    post_pk = request.POST.get('post_pk', None)

    user = User.objects.get(pk=user_id)
    # profile = Profile.objects.get(user_id=user_id)
    post = Posts.objects.get(pk=post_pk)

    if post.likes_user.filter(id=user.id).exists():
      post.likes_user.remove(user)
    else:
      post.likes_user.add(user)
    context = {'likes_count': post.count_likes_user()}
    return HttpResponse(json.dumps(context), content_type="application/json")


def note(request):
  user_id = request.session.get('user_id')

  if user_id:
    author = request.POST.get('author', None)
    contents = request.POST.get('note', None)

    from_user = User.objects.get(pk=user_id)
    to_user = User.objects.get(username=author)
    note = Note(from_user_id=from_user, to_user_id=to_user, note=contents)
    note.save()

    context = {'message': '전송되었습니다!'}
    return HttpResponse(json.dumps(context), content_type="application/json")


def mail(request):
  user_id = request.session.get('user_id')

  if user_id:
    mail_author = request.POST.get('mail_author', None)
    mail_subject = request.POST.get('mail_subject', None)
    mail_content = request.POST.get('mail_content', None)

    from_user = User.objects.get(pk=user_id)
    to_user = User.objects.get(username=mail_author)

    if mail_subject and mail_content and mail_author:
      try:
        send_mail(mail_subject, mail_content, from_user.email, [to_user.email])

        mail = Mail(mail_from_user_id=from_user.username, mail_to_user_id=to_user.username)
        mail.save()

        context = {'message': '전송되었습니다!'}
        return HttpResponse(json.dumps(context), content_type="application/json")
        
      except BadHeaderError:
        return HttpResponseRedirect('Invalid header found.')
    else:
      context = {'message': '전송되었습니다!'}
      return HttpResponse(json.dumps(context), content_type="application/json")
