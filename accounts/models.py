# accounts/models.py

from django.db import models

# Create your models here.
class User(models.Model):
  objects = models.Manager()
  name = models.CharField(max_length=200, verbose_name='이름')
  username = models.CharField(max_length=200, verbose_name='사용자명', unique=True)
  password = models.CharField(max_length=200, verbose_name='비밀번호')
  email = models.CharField(max_length=200, verbose_name='이메일')
  nickname = models.CharField(max_length=200, verbose_name='닉네임')
  following = models.ManyToManyField('self', blank=True, related_name='following_user', symmetrical=False)
  follower = models.ManyToManyField('self', blank=True, related_name='follower_user', symmetrical=False)
  blog_likes = models.ManyToManyField('self', blank=True, related_name='bloger_likes', symmetrical=False)
  created_at = models.DateTimeField(auto_now=True, verbose_name='가입날짜')
  updated_at = models.DateTimeField(auto_now=True, verbose_name='업데이트날짜')

  def __str__(self): 
    return self.username # User object 대신 나타낼 문자

  def count_following_user(self):
    return self.following.count()
  
  def count_follower_user(self):
    return self.follower.count()
  
  def count_blog_likes(self):
    return self.blog_likes.count()

  class Meta:
    db_table = 'USERS'

class Profile(models.Model):
  objects = models.Manager()
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  username = models.OneToOneField(User, to_field="username", related_name='Profile.username+', on_delete=models.CASCADE)
  introduce = models.TextField(blank=True, verbose_name='자기소개')
  profile_img = models.TextField(blank=True, verbose_name='프로필사진')
  # background_img = models.ImageField(blank=True, verbose_name='배경사진')
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')
  updated_at = models.DateTimeField(auto_now=True, verbose_name='업데이트날짜')

  class Meta:
    db_table = "PROFILE"
