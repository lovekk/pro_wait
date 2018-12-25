from django.db import models

# Create your models here.

# 失物招领
class Lose(models.Model):
    type_choices = (
        (0, '丢失'),
        (1, '捡到'),
        (2, '已领取'),
        (3, '已找到'),
    )
    first_choices = (
        (0, '未置顶'),
        (1, '置顶'),
    )
    show_choices = (
        (0, '未删除'),
        (1, '已经删除'),
    )
    content = models.CharField(max_length=300, default='', verbose_name='内容')
    view_num = models.IntegerField(verbose_name="浏览量",default=0)
    good_num = models.IntegerField(verbose_name="点赞数",default=0)
    create_date = models.DateField(auto_now_add=True, verbose_name="日期")
    create_time = models.TimeField(auto_now_add=True, verbose_name="时间")
    is_first = models.SmallIntegerField(default=0, choices=first_choices, verbose_name='置顶')
    is_type = models.SmallIntegerField(default=1, choices=type_choices, verbose_name='类型')
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否删除')
    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey('user.User',verbose_name='发布者',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_lose'
        verbose_name = "失物招领发布"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


# 相关图片
class LoseImg(models.Model):
    qiniu_img = models.CharField(max_length=100, default='', verbose_name='七牛地址')
    local_img = models.ImageField(verbose_name='本地地址', upload_to='lose/%Y/%m/%d', default='')
    lose = models.ForeignKey('Lose', verbose_name='失物招领', on_delete=models.CASCADE, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="日期时间")
    # time_stamp = models.CharField(max_length=30, default='', verbose_name="时间戳")

    class Meta:
        db_table = 'dn_lose_img'
        verbose_name = "失物招领图片"
        verbose_name_plural = verbose_name


# 评论表
class LoseComment(models.Model):
    show_choices = (
        (0, '未删除'),
        (1, '已经删除'),
    )
    content = models.CharField(max_length=100,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="评论时间")
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否删除')

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    lose = models.ForeignKey('Lose', verbose_name='失物', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'dn_lose_comment'
        verbose_name = "失物招领评论"
        verbose_name_plural = verbose_name


# 评论回复表 二级评论
class LoseReplyComment(models.Model):

    content = models.CharField(max_length=100,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="回复评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="回复评论时间")

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    lose = models.ForeignKey('Lose', verbose_name='失物', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('LoseComment', verbose_name='评论', on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', verbose_name='自关联的父级', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_lose_comment_reply'
        verbose_name = "失物招领回复评论"
        verbose_name_plural = verbose_name

