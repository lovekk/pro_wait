from django.contrib import admin
from lose.models import Lose, LoseImg, LoseComment, LoseReplyComment, RefuseLose, LoseReport


# 失物招领admin
@admin.register(Lose)
class LoseAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'content', 'view_num', 'good_num', 'create_date', 'create_time', 'is_type', 'is_first',
                    'school', 'creator']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    list_filter = ['school','is_type','is_first'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框
    # date_hierarchy = 'publish_date'  # 详细时间分层筛选　日期时间用分层筛选


# 失物招领图片
@admin.register(LoseImg)
class LoseImgAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','qiniu_img','local_img','lose','create_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 失物招领评论
@admin.register(LoseComment)
class LoseCommentAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'content', 'comment_date', 'comment_time', 'is_show', 'user', 'lose']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    list_filter = ['is_show'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框


# 失物招领 评论回复
@admin.register(LoseReplyComment)
class LoseReplyCommentAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'content', 'comment_date', 'comment_time',  'user','lose','comment','parent']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框
    # date_hierarchy = 'publish_date'  # 详细时间分层筛选　日期时间用分层筛选



# 失物招领 举报
@admin.register(LoseReport)
class LoseReportAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'lose', 'user', 'publish_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']



# 失物招领 屏蔽
@admin.register(RefuseLose)
class RefuseLoseAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'lose', 'user', 'publish_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']