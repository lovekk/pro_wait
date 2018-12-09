from django.contrib import admin
from second.models import Second,SecondImg


@admin.register(Second)
class SecondAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'content', 'view_num', 'good_num', 'report_num', 'create_date', 'create_time', 'is_type', 'is_first',
                    'is_sale', 'school', 'creator']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    list_filter = ['school', 'report_num','is_type','is_first','is_sale'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content', 'school']  # 搜索字段 标题等文本字段用搜索框
    date_hierarchy = 'create_date'  # 详细时间分层筛选　日期时间用分层筛选


@admin.register(SecondImg)
class SecondImgAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','qiniu_img','local_img','second','create_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']