from django.contrib import admin

from .models import Posts
from .models import Comments
from .models import Categories
from .models import Note
from .models import Mail

# Register your models here.
@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
  list_display = ['id', 'user_id', 'author_id', 'category_id', 'title', 'contents', 'views', 'tags', 'created_at', 'updated_at']
  list_display_links = list_display

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
  list_display = ['id', 'user_id', 'post_id', 'parent_id', 'name', 'username', 'comment', 'created_at', 'updated_at']
  list_display_links = list_display

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
  list_display = ['id', 'value', 'parent_value_id', 'name']
  list_display_links = list_display

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
  list_display = ['id', 'from_user_id', 'to_user_id', 'note', 'arrived_date']
  list_display_links = list_display


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
  list_display = ['id', 'mail_from_user_id', 'mail_to_user_id', 'arrived_date']
  list_display_links = list_display
