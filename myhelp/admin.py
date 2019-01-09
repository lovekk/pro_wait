from django.contrib import admin
from myhelp.models import Help, HelpOrder, HelpImage, HelpReport, HelpComment, HelpReplyComment, HelpCommentImage

# 发现
@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'content', 'publish_date', 'publish_time', 'status', 'price', 'is_online','is_all_school',
                    'finish_datetime','is_show', 'school', 'user']

    # 每页显示条数
    list_per_page = 100

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    list_filter = ['school','is_online','is_all_school','is_show'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框
    date_hierarchy = 'publish_date'  # 详细时间分层筛选　日期时间用分层筛选


# 订单
@admin.register(HelpOrder)
class HelpOrderAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'is_you', 'order_date', 'order_time', 'user']

    # 每页显示条数
    list_per_page = 100

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id']

    # 筛选器
    list_filter = ['is_you'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    date_hierarchy = 'order_date'  # 详细时间分层筛选　日期时间用分层筛选


# 图片
@admin.register(HelpImage)
class HelpImageAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'qiniu_img', 'local_img', 'publish_datetime', 'myhelp']

    # 每页显示条数
    list_per_page = 20

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id']


# 举报
@admin.register(HelpReport)
class HelpReportAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'myhelp', 'user', 'publish_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id']


# 评论
@admin.register(HelpComment)
class HelpCommentAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'content', 'comment_date', 'comment_time', 'is_show', 'user', 'myhelp']

    # 每页显示条数
    list_per_page = 100

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    list_filter = ['is_show'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框
    date_hierarchy = 'comment_date'  # 详细时间分层筛选　日期时间用分层筛选


# Help评论回复
@admin.register(HelpReplyComment)
class HelpReplyCommentAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'content', 'comment_date', 'comment_time', 'user', 'myhelp','comment', 'parent']

    # 每页显示条数
    list_per_page = 100

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框


# 评论图片
@admin.register(HelpCommentImage)
class HelpCommentImageAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'qiniu_img', 'local_img', 'publish_datetime', 'comment']

    # 每页显示条数
    list_per_page = 100

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id']
