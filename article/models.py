from django.db import models
from tinymce.models import HTMLField
from datetime import datetime

class Article_comment(models.Model):
    comment_date = models.DateTimeField(default=datetime.now, verbose_name="评论时间")
    content = models.TextField(max_length=200,verbose_name="评论内容",default="")
    commentator = models.ForeignKey('user.User',verbose_name='评论者',on_delete=models.CASCADE,null=True)
    article = models.ForeignKey('Article', verbose_name='文章推荐', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_article_comment'
        verbose_name = "评论"
        verbose_name_plural = verbose_name

class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name="文章标题", default="")
    content = HTMLField(verbose_name="文章内容")
    editor = models.CharField(max_length=10, verbose_name="编辑人员", default="")
    author = models.CharField(max_length=10, verbose_name="作者", default="")
    publish_date = models.DateTimeField(default=datetime.now, verbose_name="发表时间")
    view_num = models.IntegerField(verbose_name="浏览量", default=0)
    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_article'
        verbose_name = "文章推荐"
        verbose_name_plural = verbose_name


