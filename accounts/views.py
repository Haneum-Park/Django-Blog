import json

from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password 
# 비밀번호 암호화, 패스워드 체크(db와 일치성 확인)

from django.views.generic import View

from .models import User
from .models import Profile

from posts.models import Comments
from posts.models import Note
from posts.models import Mail

# Create your views here.
def signup(request):
  if request.method == "GET":
    return render(request, 'users/join.html')

  elif request.method == "POST":
    name = request.POST.get('name', None)
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    re_password = request.POST.get('re-password', None)
    email = request.POST.get('email', None)
    nickname = request.POST.get('nickname', None)
    res_data = {}
    if not (name and username and password and re_password and email):
      res_data['error'] = '모든 값을 입력해야합니다.'
    else:
      if password != re_password:
        res_data['error'] = '비밀번호가 다릅니다.'
      else:
        user = User(name=name, username=username, password=make_password(password), email=email, nickname=nickname)
        user.save()
        profile = Profile(user=user, username=user)
        profile.save()
        return redirect('/signin')
    return render(request, 'users/join.html', res_data)


def signin(request):
  response_data = {}
  try:
    request.session['signfound']
    del request.session['signfound']
  except:
    print("signfound이 없습니다.")
  user_pk = request.session.get('user_id')
  if user_pk:
    return redirect('/index')
  else:
    if request.method == "GET":
      return render(request, 'users/login.html')
    
    elif request.method == "POST":
      login_username = request.POST.get('username', None)
      login_password = request.POST.get('password', None)

      if not (login_username and login_password):
        response_data['error'] = "아이디와 비밀번호를 모두 입력해주세요."
      else:
        user = User.objects.get(username=login_username)
        # db에서 꺼내는 명령, Post로 받아온 username으로, db의 username을 꺼내온다.
        if check_password(login_password, user.password):
          request.session['user_id'] = user.id
          request.session['username'] = user.username
          request.session['nickname'] = user.nickname
          request.session['email'] = user.email
          # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
          # 세션 user 라는 key에 방금 로그인한 id를 저장한 것.
          return redirect('/index')
        else:
          response_data['error'] = '비밀번호가 틀렸습니다. 다시 입력해주세요.'
      return render(request, 'users/login.html', response_data)


def logout(request):
  print("왔다감")
  # request.session.pop('user_id')
  for key, value in list(request.session.items()):
      del request.session[key]
  # request.session.del('user')
  return redirect('/')


def update(request):
  response_data = {}
  
  user_id = request.session.get('user_id')
  if user_id:
    current_user = User.objects.get(pk=user_id)
    signfound = request.session.get('signfound')

    if request.method == "GET":
      if not signfound:
        return render(request, 'users/update.html', {'bloger': current_user})
      else:
        return render(request, 'users/update.html', {'username': signfound})

    elif request.method == "POST":
      current_username = request.session.get('username')
      current_password = request.POST.get('current_password')
      new_password = request.POST.get('new_password')
      re_new_password = request.POST.get('re_new_password')

      if not signfound:
        user = User.objects.get(username=current_username)
        if not current_password and new_password and re_new_password:
          response_data['error'] = "입력되지 않은 정보가 있습니다."
        else:
          if check_password(current_password, user.password):
            if current_password != new_password:
              if new_password == re_new_password:
                user.password = make_password(new_password)
                user.save()
                # auth.login(request, user)
                return redirect('/index')
              else:
                response_data['error'] = "새 비밀번호가 일치하지 않습니다."
            else:
              response_data['error'] = "현재 비밀번호와 새 비밀번호가 일치합니다. 다시 입력해주세요."
          else:
            response_data['error'] = "현재 비밀번호가 일치하지 않습니다."

        return render(request, 'users/update.html', {
          'error': response_data['error'], 
          'user': current_user
        })
      else:
        user = User.objects.get(username=signfound)
        if new_password == re_new_password:
          user.password = make_password(new_password)
          user.save()
          del request.session['user_id']
          del request.session['signfound']
          return redirect('/signin')
        else:
          response_data['error'] = "새 비밀번호가 일치하지 않습니다."
          return render(request, 'users/update.html', {
            'error': response_data['error'],
            'username': signfound
          })
  else:
    return redirect('/signin')


def profile(request):
  user_id = request.session.get('user_id')
  if not user_id:
    return redirect('/signin')
  else:
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user_id=user_id)

    if request.method == "GET":
      return render(request, 'users/profile.html', {
        'bloger': user,
        'profile': profile
      })

    elif request.method == "POST":
      nickname = request.POST.get('nickname')
      introduce = request.POST.get('introduce')
      profile_img = request.POST.get('profile_img')

      user.nickname = nickname
      profile.introduce = introduce
      # profile.profile_img = profile_img

      user.save()
      profile.save()

      try:
        comments = Comments.objects.filter(user_id=user_id)
        comments.nickname = nickname
        comments.save()
      except:
        print("댓글에 대한 닉네임이 없습니다.")
      
      return redirect('/index')


def secession(request):
  user_id = request.session.get('user_id')
  user = User.objects.get(pk=user_id)

  user.delete()
  for key, value in list(request.session.items()):
    del request.session[key]
  return redirect('/')


def signfind(request):
  response_data = {}

  user_id = request.session.get('user_id')
  signfound = request.session.get('signfound')
  if not user_id:
    if signfound:
      if request.method == "GET":
        return render(request, 'users/signfind.html', {'signfound': signfound})
      elif request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        if not username:
          try:
            user = User.objects.get(name=name, email=email)

            request.session['signfound'] = user.username
          except:
            response_data['error'] = "입력하신 정보와 일치하는 계정이 없습니다."
            return render(request, 'users/signfind.html', response_data)
          return redirect('/signfound')
        else:
          try:
            user = User.objects.get(name=name, email=email, username=username)
            request.session['user_id'] = user.id
          except:
            response_data['error'] = "입력하신 정보와 일치하는 계정이 없습니다."
            return render(request, 'users/signfind.html', response_data)
          return redirect('/update')
    else:
      return render(request, 'users/signfind.html')
    
  else:
    return redirect('/index')


def signfound(request):
  user_id = request.session.get('user_id')

  if not user_id:
    signfound = request.session.get('signfound')
    return render(request, 'users/signfound.html', {'signfound': signfound})

  else:
    return redirect('/index')


def following(request, username):
  user_id = request.session.get('user_id')

  if user_id:
    user = User.objects.get(pk=user_id)  # 팔로우를 한 유저. 즉, from
    blog_author_id = request.POST.get('blog_author_id', None)

    blog_author = User.objects.get(pk=blog_author_id)  # 팔로우를 받은 유저. 즉, to
   
    if user.following.filter(id=blog_author.id).exists() and blog_author.follower.filter(id=user.id).exists():
      user.following.remove(blog_author.id)
      blog_author.follower.remove(user.id)
    else:
      user.following.add(blog_author.id)
      blog_author.follower.add(user.id)
    context = {'following_count': user.count_following_user(), 'follower_count': blog_author.count_follower_user()}

    return HttpResponse(json.dumps(context), content_type='application/json')


def blogLike(request, username):
  user_id = request.session.get('user_id')

  if user_id:
    blog_author_id = request.POST.get('blog_author_id', None)

    user = User.objects.get(pk=user_id)
    blog_author = User.objects.get(pk=blog_author_id)

    if blog_author.blog_likes.filter(id=user.id).exists():
      blog_author.blog_likes.remove(user.id)
    else:
      blog_author.blog_likes.add(user.id)

    context = {'like_count': blog_author.count_blog_likes()}

    return HttpResponse(json.dumps(context), content_type='application/json')
