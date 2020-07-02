from django.db.models import Q

from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

from accounts.models import User
from accounts.models import Profile

from posts.models import Posts
from posts.models import Note
from posts.models import Mail

# Create your views here.
def application(request):
  posts = Posts.objects.all()

  context = {}

  if len(posts) == 0:
    context['message'] = "게시된 포스트가 없습니다."
  else:
    context['posts'] = posts

  return render(request, 'main/index.html', context)


def index(request):
  # for key, value in list(request.session.items()):
  #     del request.session[key]
  user_id = request.session.get('user_id')  # 하나만 가져오기
  if user_id:
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    note = Note.objects.filter(to_user_id=user.username)
    mail = Mail.objects.filter(mail_to_user_id=user.username)
    
    context = {'bloger': user, 'profile': profile, 'note': note, 'mail': mail}
    
    posts = Posts.objects.all()  # 모두 가져오기

    if len(posts) == 0:
      context['message'] = "게시된 포스트가 없습니다."
    else:
      context['posts'] = posts

    return render(request, 'main/index.html', context)
  else:
    return redirect('/')


def tagSearch(request, tag):
  posts = None

  user_id = request.session.get('user_id')

  user = User.objects.get(pk=user_id)
  profile = Profile.objects.get(user_id=user_id)
  note = Note.objects.filter(to_user_id=user.username)
  mail = Mail.objects.filter(mail_to_user_id=user.username)

  context = {'bloger': user, 'profile': profile, 'note': note, 'mail': mail}

  posts = Posts.objects.all().filter(Q(tags__contains=tag))

  if len(posts) == 0:
    context['message'] = "태그와 관련된 게시글이 존재하지 않습니다."
  else:
    context['posts'] = posts

  return render(request, 'main/index.html', context)


def noteBox(request, username):
  user_id = request.session.get('user_id')

  if user_id:
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    note = Note.objects.filter(to_user_id=user.username)
    mail = Mail.objects.filter(mail_to_user_id=user.username)

    context = {'bloger': user, 'profile': profile, 'note': note, 'mail': mail}

    notes = Note.objects.filter(to_user_id=user.username)
    
    if len(notes) == 0:
      context['message'] = "받은 쪽지가 없습니다."
    else:
      context['notes'] = notes

    return render(request, 'note/index.html', context)
  else:
    redirect('/signin')


def noteNew(request, username):
  user_id = request.session.get('user_id')
  if user_id:
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)
    note = Note.objects.filter(to_user_id=user.username)
    mail = Mail.objects.filter(mail_to_user_id=user.username)
    users = User.objects.all()

    context = {'bloger': user, 'profile': profile, 'note': note, 'mail': mail, 'blogers': users}

    if request.method == "GET":
      return render(request, 'note/new.html', context)
    elif request.method == "POST":
      return render(request, 'note/index.html', context)
  else:
    redirect('/signin')


def noteDelete(request, username, pk):
  user_id = request.session.get('user_id')

  if user_id:
    note = Note.objects.get(pk=pk, to_user_id=username)
    print(note)
    note.delete()

    return redirect('/' + username + '/notebox/index')

  else:
    redirect('/signin')
    
