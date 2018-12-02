
from django.contrib import admin
from user.models import User, School

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



# admin.site.register(User, UserAdmin)
# admin.site.register(School, SchoolAdmin)


