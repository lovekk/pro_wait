
from django.contrib import admin
from user.models import User, School, Follow, FunctionModule,RecoveryPerson,AboutWe,AboutWeComment,Login

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','phone_num','password','nick','gender','school_name','my_sign','real_name','account_num',
                    'integral','is_real_name_auth','is_school_auth','stu_num','stu_password','reg_ip','channel',
                    'system_type','device_num','device_model','device_name','operator','create_date','good_total',
                    'comment_total','fans_total','create_total','head_image','head_qn_url','token']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'phone_num']


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'name', 'province', 'city', 'is_show', 'is_enter']

    # 每页显示条数
    list_per_page = 20

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
    list_display = ['id', 'user', 'follow_id', 'is_delete','create_date']

    # 每页显示条数
    list_per_page = 10

    # id 排序
    ordering = ['-id']

    # 列表上方搜索框
    search_fields = ['user']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'user']


@admin.register(FunctionModule)
class FunctionModuleAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'module_name', 'create_datetime','school']

    # 每页显示条数
    list_per_page = 20

    # id 排序
    ordering = ['id']

    # 列表上方搜索框
    search_fields = ['module_name']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'module_name']

# admin.site.register(User, UserAdmin)
# admin.site.register(School, SchoolAdmin)


# 回收人员
@admin.register(RecoveryPerson)
class RecoveryPersonAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'log_num', 'password', 'school','is_use']

    # 每页显示条数
    list_per_page = 10

    # id 排序
    ordering = ['-id']

    # 列表上方搜索框
    search_fields = ['log_num']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'log_num']


# 关于我们
@admin.register(AboutWe)
class AboutWeAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'title', 'content', 'create_date']

    # 每页显示条数
    list_per_page = 10

    # id 排序
    ordering = ['id']

    # 列表上方搜索框
    search_fields = ['log_num']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'title']


# 关于我们-评论
@admin.register(AboutWeComment)
class AboutWeCommentAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'comment', 'create_date', 'create_time','is_delete','user']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 列表上方搜索框
    search_fields = ['comment']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'comment']


# 登录
@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_num', 'password', 'log_ip','device_num','device_model','device_name','operator','channel',
                    'system_type','system_version','connection_type','screen_width','screen_height','jail_break','user']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 列表上方搜索框
    search_fields = ['phone_num']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'phone_num']