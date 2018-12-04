from django.contrib import admin
from notice.models import Notice


@admin.register(Notice)
class Notice(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','content','editor','publish_date','view_num','school']

    # 每页显示条数
    list_per_page = 10

    # id 正序
    ordering = ['id']









