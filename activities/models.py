from django.db import models
from tinymce.models import HTMLField
from datetime import datetime


class Activites_comment(models.Model):
    comment_date = models.DateTimeField(default=datetime.now, verbose_name="评论时间")
    content = models.TextField(max_length=200,verbose_name="评论内容",default="")
    commentator = models.ForeignKey('user.User',verbose_name='评论者',on_delete=models.CASCADE,null=True)
    activites = models.ForeignKey('Activites', verbose_name='校园活动', on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = 'dn_activites_comment'
        verbose_name = "评论"
        verbose_name_plural = verbose_name

class Activites(models.Model):
    title = models.CharField(max_length=50,verbose_name="活动标题",default="")
    introduction = models.CharField(max_length=100,verbose_name="活动简介",default="")
    content = HTMLField(verbose_name="活动内容")
    editor = models.CharField(max_length=10,verbose_name="编辑人员",default="")
    publish_date = models.DateTimeField(default=datetime.now, verbose_name="发表时间")
    view_num = models.IntegerField(verbose_name="浏览量",default=0)
    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_activites'
        verbose_name = "校园活动"
        verbose_name_plural = verbose_name
