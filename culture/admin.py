from django.contrib import admin
from culture.models import CultureComment,Culture


@admin.register(Culture)
class Culture(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','short_introduction','short_content','editor','view_num','comment_num','school',
                    'publish_date','create_date']

    # 每页显示条数
    list_per_page = 20

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'title']

    # 筛选器
    list_filter = ['school','editor'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['title']  # 搜索字段 标题等文本字段用搜索框


@admin.register(CultureComment)
class Culture_comment(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','content','commentator','culture','create_date','comment_date']

    # 每页显示条数
    list_per_page = 100

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    list_filter = ['culture'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框







