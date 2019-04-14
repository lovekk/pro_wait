from django.contrib import admin
from second.models import Second,SecondImg,SecondComment,SecondReplyComment,SecondReport,RefuseSecond


# 二手市场
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
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框


# 二手市场 图片
@admin.register(SecondImg)
class SecondImgAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','qiniu_img','local_img','second','create_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 二手市场 评论
@admin.register(SecondComment)
class SecondCommentAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'content','comment_date', 'comment_time', 'is_show', 'replay_num', 'user', 'second']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    list_filter = ['is_show']  # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框
    # date_hierarchy = 'publish_date'  # 详细时间分层筛选　日期时间用分层筛选


# 二手市场 评论回复
@admin.register(SecondReplyComment)
class SecondReplyCommentAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'content', 'comment_date', 'comment_time', 'user', 'second', 'comment', 'parent']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框
    # date_hierarchy = 'publish_date'  # 详细时间分层筛选　日期时间用分层筛选


# 二手市场 举报
@admin.register(SecondReport)
class SecondReportAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'second', 'user', 'publish_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']



# 屏蔽 二手
@admin.register(RefuseSecond)
class RefuseSecondAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'second', 'user', 'publish_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

