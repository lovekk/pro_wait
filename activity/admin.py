from django.contrib import admin
from activity.models import Activity,ActivityComment


# 校园活动admin
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','title','is_first','is_show','short_content','editor','view_num','school','publish_date','create_date']

    # 每页显示条数
    list_per_page = 20

    # id 正序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'title']

    # 筛选器
    list_filter = [ 'title', 'school'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['title', 'school']  # 搜索字段 标题等文本字段用搜索框


# 校园活动评论admin
@admin.register(ActivityComment)
class ActivityCommentAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','content','commentator','activity','comment_date']

    # 每页显示条数
    list_per_page = 50

    # id 正序
    ordering = ['-id']

    list_filter = ['activity']  # 过滤器  一般ManyToManyField多对多字段用过滤器