# posts/models.py

from django.db import models
from accounts.models import User

from tagging.fields import TagField

# Create your models here.
class Categories(models.Model):
  objects = models.Manager()
  value = models.IntegerField(verbose_name="카테고리 ID", default=0)
  parent_value = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name="부모아이디")
  name = models.CharField(max_length=200, verbose_name="카테고리명", default='')

  def __str__(self):
      return self.name
  

  class Meta:
    db_table = "CATEGORIES"


class Posts(models.Model):
  objects = models.Manager()
  user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, related_name="user_id")
  author = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, unique=False, related_name="user_username")
  category = models.ForeignKey(Categories, on_delete=models.CASCADE, unique=False, default='')
  title = models.CharField(max_length=200, verbose_name='제목', help_text="최대 200자 내로 입력하세요.")
  contents = models.TextField(verbose_name='내용')
  views = models.PositiveIntegerField(verbose_name="조회수", default=0)
  likes_user = models.ManyToManyField(User, blank=True, related_name='likes_user')
  tags = TagField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def count_likes_user(self):
    return self.likes_user.count()
  
  def summary(self): # 100자이상 more...
    return self.contents[:100]

  class Meta:
    db_table = "POSTS"
    

class Comments(models.Model):
  objects = models.Manager()
  user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
  post = models.ForeignKey(Posts, on_delete=models.CASCADE, unique=False)
  parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name='대댓글')
  name = models.CharField(max_length=200, verbose_name='이름', default='')
  username = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, verbose_name='닉네임', related_name='Comments.username+', default='')
  comment = models.TextField(verbose_name="댓글", default='')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "COMMENTS"


class Note(models.Model):
  objects = models.Manager()
  from_user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, unique=False, related_name='보낸사람', default='')
  to_user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, unique=False, related_name='받는사람', default='')
  note = models.TextField(verbose_name='내용')
  arrived_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = "NOTE"


class Mail(models.Model):
  objects = models.Manager()
  mail_from_user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, unique=False, related_name='메일보낸사람', default='')
  mail_to_user = models.ForeignKey(User, to_field='username',on_delete=models.CASCADE, unique=False, related_name='메일받는사람', default='')
  arrived_date = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = "MAIL"
