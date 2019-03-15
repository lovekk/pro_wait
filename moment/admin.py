from django.contrib import admin
from moment.models import Moment, Voice, Video, Image, Good, Comment, ReplyComment, Tag, Report, CommentGood
from moment.models import CommentImage, CommentVoice, CommentVideo, Push

# 发现
@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id', 'content', 'tag', 'user', 'school','is_show', 'good_num', 'comment_num', 'view_num', 'relay_num',
                    'report_num', 'is_first', 'publish_date', 'publish_time']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'content']

    # 筛选器
    list_filter = ['school', 'tag', 'report_num', 'is_show'] # 过滤器  一般ManyToManyField多对多字段用过滤器
    search_fields = ['content']  # 搜索字段 标题等文本字段用搜索框
    date_hierarchy = 'publish_date'  # 详细时间分层筛选　日期时间用分层筛选


# 发现音频
@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','qiniu_voice','local_voice', 'voice_time', 'publish_datetime','moment']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 发现视频
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):

    # 显示的字段
    list_display = ['id','qiniu_video','local_video','publish_datetime','moment']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 发现图片
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'qiniu_img', 'local_img', 'publish_datetime', 'moment']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 发现标签
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'name', 'add_time']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['id']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'name']


# 点赞
@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'user', 'moment', 'crate_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 评论
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'content', 'comment_date', 'comment_time', 'good_num', 'user', 'moment']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 回复评论
@admin.register(ReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'content', 'comment_date', 'comment_time', 'user', 'comment', 'moment']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 评论点赞
@admin.register(CommentGood)
class GoodAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'user', 'comment', 'crate_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 举报
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'moment', 'user', 'publish_datetime']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 评论图片
@admin.register(CommentImage)
class CommentImageAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'qiniu_img', 'local_img', 'publish_datetime', 'comment']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 回复语音
@admin.register(CommentVoice)
class CommentVoiceAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'qiniu_voice', 'local_voice', 'voice_time', 'publish_datetime', 'comment']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 评论 视频
@admin.register(CommentVideo)
class CommentVideoAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'qiniu_video', 'local_video', 'qiniu_video_img', 'local_video_img',
                    'video_size', 'publish_datetime','comment']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']


# 推送
@admin.register(Push)
class PushAdmin(admin.ModelAdmin):
    # 显示的字段
    list_display = ['id', 'push_content', 'comment_date', 'comment_time', 'push_type',
                    'publish_id', 'publisher_id','commentator']

    # 每页显示条数
    list_per_page = 50

    # id 排序
    ordering = ['-id']