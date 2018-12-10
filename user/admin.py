
from django.contrib import admin
from user.models import User, School, Follow

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','phone_num','password','nick','gender','head_image','school_name','token',
                    'device_num','integral','create_date','is_school_auth','is_real_name_auth']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'name', 'province', 'city', 'is_show', 'is_enter']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']

    # name字段全部显示到右侧边栏
    list_filter = ['name']

    # 列表上方搜索框
    search_fields = ['name']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'name']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'user', 'follow_id', 'create_date']

    # 每页显示条数
    list_per_page = 10

    # id 排序
    ordering = ['-id']

    # 列表上方搜索框
    search_fields = ['user']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'user']




# admin.site.register(User, UserAdmin)
# admin.site.register(School, SchoolAdmin)


