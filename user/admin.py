
from django.contrib import admin
from user.models import User, School, Follow, FunctionModule,RecoveryPerson,AboutWe,AboutWeComment,Login,IntegralGoods,IntegralOrder

# Register your models here.


# 用户 信息
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','phone_num','password','nick','gender','school_name','my_sign','real_name','account_num',
                    'integral','is_real_name_auth','is_school_auth','stu_num','stu_password','reg_ip','channel',
                    'system_type','device_num','device_model','device_name','operator','create_date','good_total',
                    'comment_total','fans_total','create_total','find_total','help_total','head_image','head_qn_url','token']

    # 每页显示条数
    list_per_page = 50

    # id 正序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'phone_num']

    search_fields = ['phone_num', 'nick']  # 搜索字段 标题等文本字段用搜索框

    list_filter = ['school_name','is_school_auth','is_real_name_auth']  # 过滤器  字段全部显示到右侧边栏


# 用户 学校列表
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'name', 'province', 'city', 'is_show', 'is_enter']

    # 每页显示条数
    list_per_page = 20

    # id 正序
    ordering = ['id']

    # name字段全部显示到右侧边栏
    list_filter = ['name','city','is_show']

    # 列表上方搜索框
    search_fields = ['name']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'name']



# 用户 关注
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'user', 'follow_id', 'is_delete','create_date']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 列表上方搜索框
    search_fields = ['user']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'user']

    list_filter = ['is_delete']  # 过滤器  字段全部显示到右侧边栏


# 学校 模块
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

    list_filter = ['module_name']  # 过滤器  字段全部显示到右侧边栏



# 回收人员
@admin.register(RecoveryPerson)
class RecoveryPersonAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'log_num', 'password', 'school','is_use']

    # 每页显示条数
    list_per_page = 20

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
    list_display = ['id', 'phone_num', 'password','user', 'log_ip','device_num','device_model','device_name','operator','channel',
                    'system_type','system_version','connection_type','screen_width','screen_height','jail_break','create_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 列表上方搜索框
    search_fields = ['phone_num']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'phone_num']


# 积分商城  2019/2/19
@admin.register(IntegralGoods)
class IntegralGoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'desc','image']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['id']


# 兑换订单  2019/2/19
@admin.register(IntegralOrder)
class IntegralOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_num', 'address','good','status','which_school','user', 'create_date','change_date']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 列表上方搜索框
    search_fields = ['phone_num']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'phone_num']

    # name字段全部显示到右侧边栏
    list_filter = ['which_school','status']


# admin.site.register(User, UserAdmin)
# admin.site.register(School, SchoolAdmin)

