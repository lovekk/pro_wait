from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from datetime import datetime
import user


# 校园文化
class Culture(models.Model):
    title = models.CharField(max_length=50,verbose_name="文化标题",default="")
    introduction = models.TextField(verbose_name="文化简介",default="")
    content = HTMLField(verbose_name="文化内容")
    editor = models.CharField(max_length=10,verbose_name="编辑人员",default="")
    publish_date = models.DateField(auto_now_add=True, verbose_name="发表日期")
    create_date = models.DateTimeField(auto_now_add=True,verbose_name="发表时间")
    view_num = models.IntegerField(verbose_name="浏览量",default=0)
    comment_num = models.IntegerField(verbose_name="评论数",default=0)

    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_culture'
        verbose_name = "校园文化"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # 指定字段内容长度，超出部分。。。代替
    def short_introduction(self):
        if len(str(self.introduction)) > 200:
            return '{}......'.format(str(self.introduction)[0:200])
        else:
            return str(self.introduction)
    short_introduction.allow_tags = True
    short_introduction.short_description = u"文化简介"

    # 指定字段内容长度，超出部分。。。代替
    def short_content(self):
        if len(str(self.content)) > 500:
            return '{}......'.format(str(self.content)[0:500])
        else:
            return str(self.content)
    short_content.allow_tags = True
    short_content.short_description = u"文化内容"


# 校园文化评论
class CultureComment(models.Model):
    show_choices = (
        (0, '显示'),
        (1, '不显示'),
    )
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建日期")
    content = models.CharField(max_length=100,verbose_name="评论内容",default="")
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否显示')

    commentator = models.ForeignKey('user.User',verbose_name='评论者',on_delete=models.CASCADE,null=True)
    culture = models.ForeignKey('Culture', verbose_name='校园文化', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_culture_comment'
        verbose_name = "校园文化·评论"
        verbose_name_plural = verbose_name
