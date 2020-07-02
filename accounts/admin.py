from django.contrib import admin
from .models import User # 같은 경로의 models.py 에서 User라는 클래스를 import 
from .models import Profile

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'username', 'password', 'email', 'nickname', 'created_at']
  list_display_links = list_display

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['id', 'username', 'introduce', 'profile_img', 'created_at', 'updated_at', 'user_id']
  list_display_links = list_display


# list_display: Admin 목록에 보여질 필드 목록
# list_display_links: 목록 내에서 링크로 지정할 필드 목록(이를 지정하지 않으면, 첫번째 필드에만 링크가 적용)
# list_editable: 목록 상에서 수정할 필드 목록
# list_per_page: 페이지 별로 보여질 최대 갯수(디폴트: 100)
# list_filter: 필터 옵션을 제공할 필드 목록
# actions: 목록에서 수행할 action 목록
