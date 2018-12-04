from django.db import models
from tinymce.models import HTMLField
from datetime import datetime

class Notice(models.Model):
    title = models.CharField(max_length=50, verbose_name="公告标题", default="")
    content = HTMLField(verbose_name="公告内容")
    editor = models.CharField(max_length=10, verbose_name="编辑人员", default="")
    publish_date = models.DateField(default=datetime.now, verbose_name="发表时间")
    view_num = models.IntegerField(verbose_name="浏览量", default=0)
    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_notice'
        verbose_name = "校园公告"
        verbose_name_plural = verbose_name
