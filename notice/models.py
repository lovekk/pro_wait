from django.db import models
from tinymce.models import HTMLField
from datetime import datetime

class Notice(models.Model):
    show_choices = (
        (0, '显示'),
        (1, '不显示'),
    )
    title = models.CharField(max_length=60, verbose_name="公告标题", default="")
    content = HTMLField(verbose_name="公告内容")
    editor = models.CharField(max_length=10, verbose_name="编辑人员", default="")
    publish_date = models.DateField(default=datetime.now, verbose_name="发表时间")
    view_num = models.IntegerField(verbose_name="浏览量", default=0)
    sort_num = models.IntegerField(verbose_name="排序", default=0)
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否显示')

    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_notice'
        verbose_name = "校园公告"
        verbose_name_plural = verbose_name

    # 指定字段内容长度，超出部分。。。代替
    def short_content(self):
        if len(str(self.content)) > 500:
            return '{}...'.format(str(self.content)[0:500])
        else:
            return str(self.content)
    short_content.allow_tags = True
    short_content.short_description = u"公告内容"
