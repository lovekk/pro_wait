from django.db import models

from datetime import datetime

# =======================================================发现=====================================================
# 发现表
class Moment(models.Model):
    first_choices = (
        (0, '未置顶'),
        (1, '置顶'),
    )
    show_choices = (
        (0, '未删除'),
        (1, '已经删除'),
    )
    global_choices = (
        (0, '不同步'),
        (1, '同步全国'),
    )
    content = models.CharField(max_length=500, verbose_name="动态内容", default="")
    publish_date = models.DateField(auto_now_add=True, verbose_name="发表日期")
    publish_time = models.TimeField(auto_now_add=True, verbose_name="发表时间")
    tag = models.CharField(max_length=30,verbose_name="标签",default="")
    good_num = models.IntegerField(verbose_name="点赞数量",default=0)
    comment_num = models.IntegerField(verbose_name="评论数量",default=0)
    view_num = models.IntegerField(verbose_name="浏览量",default=0)
    relay_num = models.IntegerField(verbose_name="转发量",default=0)
    report_num = models.IntegerField(verbose_name="举报数", default=0)
    is_first = models.SmallIntegerField(default=0, choices=first_choices, verbose_name='置顶')
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否删除')
    is_global = models.SmallIntegerField(default=1, choices=global_choices, verbose_name='是否同步全国')

    school = models.ForeignKey('user.School',verbose_name='学校',on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'dn_moment'
        verbose_name = "发现·动态内容"
        verbose_name_plural = verbose_name


# 音频表
class Voice(models.Model):
    qiniu_voice = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_voice = models.FileField(verbose_name="本地地址",upload_to='moment_voice/%Y/%m/%d',default="")
    voice_time = models.CharField(max_length=20, verbose_name="音频时长", default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    moment = models.OneToOneField('Moment', verbose_name='发现id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_voice'
        verbose_name = "发现·语音"
        verbose_name_plural = verbose_name


# 视频表
class Video(models.Model):
    qiniu_video = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_video = models.FileField(verbose_name="本地地址",upload_to='moment_video/%Y/%m/%d',default="")
    qiniu_video_img = models.CharField(max_length=100, verbose_name="七牛云视频缩略图", default="")
    local_video_img = models.ImageField(verbose_name="本地视频缩略图",upload_to='moment_video/%Y/%m/%d',default="")
    video_size = models.CharField(max_length=20, verbose_name="视频大小", default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    moment = models.ForeignKey('Moment', verbose_name='发现id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_video'
        verbose_name = "发现·视频"
        verbose_name_plural = verbose_name


# 图片表
class Image(models.Model):
    qiniu_img = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_img = models.ImageField(verbose_name="本地地址",upload_to='moment_img/%Y/%m/%d',default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    moment = models.ForeignKey('Moment', verbose_name='发现id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_image'
        verbose_name = "发现·图片"
        verbose_name_plural = verbose_name


# 发现点赞表
class Good(models.Model):
    crate_datetime = models.DateTimeField(auto_now_add=True, verbose_name="点赞时间")

    user = models.ForeignKey('user.User', verbose_name='关联用户id',on_delete=models.CASCADE, null=True)
    moment = models.ForeignKey('Moment', verbose_name='关联发现id',on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_good'
        verbose_name = "发现·点赞"
        verbose_name_plural = verbose_name



# =======================================================评论=====================================================
# 评论表
class Comment(models.Model):
    show_choices = (
        (0, '未删除'),
        (1, '已经删除'),
    )
    content = models.CharField(max_length=100,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="评论时间")
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否删除')
    good_num = models.IntegerField(verbose_name="点赞数量",default=0)
    replay_num = models.IntegerField(verbose_name="评论回复数量",default=0)

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    moment = models.ForeignKey('Moment', verbose_name='发现', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'dn_moment_comment'
        verbose_name = "发现·评论"
        verbose_name_plural = verbose_name


# 评论 图片表
class CommentImage(models.Model):
    qiniu_img = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_img = models.ImageField(verbose_name="本地地址",upload_to='moment_comment_img/%Y/%m/%d',default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    comment = models.ForeignKey('Comment', verbose_name='评论id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_comment_image'
        verbose_name = "发现·评论·图片"
        verbose_name_plural = verbose_name


# 评论 音频表
class CommentVoice(models.Model):
    qiniu_voice = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_voice = models.FileField(verbose_name="本地地址",upload_to='moment_comment_voice/%Y/%m/%d',default="")
    voice_time = models.CharField(max_length=20, verbose_name="音频时长", default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    comment = models.OneToOneField('Comment', verbose_name='评论id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_comment_voice'
        verbose_name = "发现·评论·语音"
        verbose_name_plural = verbose_name


# 评论 视频表
class CommentVideo(models.Model):
    qiniu_video = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_video = models.FileField(verbose_name="本地地址",upload_to='moment_comment_video/%Y/%m/%d',default="")
    qiniu_video_img = models.CharField(max_length=100, verbose_name="七牛云视频缩略图", default="")
    local_video_img = models.ImageField(verbose_name="本地视频缩略图",upload_to='moment_video/%Y/%m/%d',default="")
    video_size = models.CharField(max_length=20, verbose_name="视频大小", default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    comment = models.ForeignKey('Comment', verbose_name='评论id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_comment_video'
        verbose_name = "发现·评论·视频"
        verbose_name_plural = verbose_name



# 评论 点赞表
class CommentGood(models.Model):
    crate_datetime = models.DateTimeField(auto_now_add=True, verbose_name="点赞时间")

    user = models.ForeignKey('user.User', verbose_name='关联用户id',on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comment', verbose_name='关联评论id',on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_comment_good'
        verbose_name = "发现·评论点赞"
        verbose_name_plural = verbose_name



# 评论回复表 二级评论
class ReplyComment(models.Model):

    content = models.CharField(max_length=100,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="回复评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="回复评论时间")

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    moment = models.ForeignKey('Moment', verbose_name='发现', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comment', verbose_name='评论', on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', verbose_name='自关联的父级', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_moment_comment_reply'
        verbose_name = "发现·回复评论"
        verbose_name_plural = verbose_name


# =======================================================其他=====================================================
# 标签表
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name="标签名称", default="")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = 'dn_moment_tag'
        verbose_name = "发现·标签"
        verbose_name_plural = verbose_name


# 举报表
class Report(models.Model):
    moment = models.ForeignKey('moment',verbose_name='发现id',on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='用户id', on_delete=models.CASCADE, null=True)
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = 'dn_moment_report'
        verbose_name = "发现·举报"
        verbose_name_plural = verbose_name


