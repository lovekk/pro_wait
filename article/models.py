from django.db import models
from tinymce.models import HTMLField
from datetime import datetime


# 文章
class Article(models.Model):
    show_choices = (
        (0, '不显示'),
        (1, '显示'),
    )
    all_school = (
        (0, '不同步'),
        (1, '同步全国'),
    )
    my_original = (
        (0, '不是原创'),
        (1, '原创'),
    )
    title = models.CharField(max_length=100, verbose_name="文章标题", default="")
    list_img = models.ImageField(upload_to='article/%Y/%m', verbose_name="文章头像", default="")
    content = HTMLField(verbose_name="文章内容")
    editor = models.CharField(max_length=30, verbose_name="编辑人员", default="")
    author = models.CharField(max_length=30, verbose_name="作者", default="")
    publish_date = models.DateField(default=datetime.now, verbose_name="发表日期")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    view_num = models.IntegerField(verbose_name="浏览量", default=0)
    is_show = models.SmallIntegerField(default=1, choices=show_choices, verbose_name='显示')
    is_all_school = models.SmallIntegerField(default=0, choices=all_school, verbose_name='同步全国')
    is_original = models.SmallIntegerField(default=0, choices=my_original, verbose_name='原创')

    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_article'
        verbose_name = "九点读书·文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # 指定字段内容长度，超出部分。。。代替
    def short_content(self):
        if len(str(self.content)) > 500:
            return '{}...'.format(str(self.content)[0:500])
        else:
            return str(self.content)
    # 注意, allow_tags属性, 其默认值是False, 如果错误使用将会带来安全隐患. 如果设置为True,
    # 在admin中会允许显示HTML tag. 因此我们使用的原则是, 对于用户输入的信息, 永远不设置allow_tags=True.
    # 只有当其内容是管理员/系统生成, 用户无法修改的时, 才能使用allow_tags=True.
    short_content.allow_tags = True


# 评论
class ArticleComment(models.Model):
    comment_datetime = models.DateTimeField(default=datetime.now, verbose_name="评论时间")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建日期")
    content = models.CharField(max_length=300,verbose_name="评论内容",default="")
    commentator = models.ForeignKey('user.User',verbose_name='评论者',on_delete=models.CASCADE,null=True)
    article = models.ForeignKey('Article', verbose_name='文章推荐', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_article_comment'
        verbose_name = "九点读书·评论"
        verbose_name_plural = verbose_name


