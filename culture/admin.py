from django.contrib import admin
from culture.models import Culture_comment,Culture


@admin.register(Culture_comment)
class Culture_comment(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','comment_date','content','commentator','culture']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']

@admin.register(Culture)
class Culture(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','introduction','content','editor','publish_date','view_num','school']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']







