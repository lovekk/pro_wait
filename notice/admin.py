from django.contrib import admin
from notice.models import Notice


@admin.register(Notice)
class Notice(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','short_content','editor','publish_date','view_num','school']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'title']

    # 筛选器
    list_filter = ['school'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['title']  # 搜索字段 标题等文本字段用搜索框
    date_hierarchy = 'publish_date'  # 详细时间分层筛选　日期时间用分层筛选









