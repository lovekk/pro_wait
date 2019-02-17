from django.db import models
from tinymce.models import HTMLField
from datetime import datetime


# 活动评论
class ActivityComment(models.Model):
    show_choices = (
        (0, '显示'),
        (1, '已删除'),
    )
    comment_date = models.DateField(auto_now_add=True, verbose_name="创建日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="创建时间")
    content = models.CharField(max_length=100,verbose_name="评论内容",default="")
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否显示')

    commentator = models.ForeignKey('user.User',verbose_name='评论者',on_delete=models.CASCADE,null=True)
    activity = models.ForeignKey('Activity', verbose_name='校园活动', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_activity_comment'
        verbose_name = "校园活动·评论"
        verbose_name_plural = verbose_name

# 活动
class Activity(models.Model):
    first_choices = (
        (0, '未置顶'),
        (1, '置顶'),
    )
    show_choices = (
        (0, '不显示'),
        (1, '显示'),
    )
    title = models.CharField(max_length=50,verbose_name="活动标题",default="")
    big_img = models.ImageField(verbose_name='首页轮播图', upload_to='activity/%Y/%m', default='')
    small_img = models.ImageField(verbose_name='列表图', upload_to='activity/%Y/%m', default='')
    introduction = models.TextField(verbose_name="活动简介",default="")
    content = HTMLField(verbose_name="活动内容")
    host_unit = models.CharField(max_length=30,verbose_name="主办方",default="官方")
    editor = models.CharField(max_length=10,verbose_name="编辑人员",default="")
    publish_date = models.DateField(default=datetime.now, verbose_name="发表日期")
    create_date = models.DateTimeField(default=datetime.now, verbose_name="创立时间")
    view_num = models.IntegerField(verbose_name="浏览量",default=0)
    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)
    is_first = models.SmallIntegerField(default=0, choices=first_choices, verbose_name='置顶')
    is_show = models.SmallIntegerField(default=1, choices=show_choices, verbose_name='显示')

    class Meta:
        db_table = 'dn_activity'
        verbose_name = "校园活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


    # 指定字段内容长度，超出部分。。。代替
    def short_content(self):
        if len(str(self.content)) > 500:
            return '{}...'.format(str(self.content)[0:500])
        else:
            return str(self.content)
    short_content.allow_tags = True
    short_content.short_description = u"活动内容"
