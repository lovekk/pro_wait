from django.contrib import admin
from culture.models import CultureComment,Culture


@admin.register(CultureComment)
class Culture_comment(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','create_date','comment_date','content','commentator','culture']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']



@admin.register(Culture)
class Culture(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','short_introduction','short_content','editor','publish_date','create_date','view_num','school']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']







