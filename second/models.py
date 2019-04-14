from django.db import models

# Create your models here.

# 二手市场
class Second(models.Model):
    type_choices = (
        (0, '全新'),
        (1, '九新'),
        (2, '半新'),
    )
    first_choices = (
        (0, '未置顶'),
        (1, '置顶'),
    )
    sale_choices = (
        (0, '未售出'),
        (1, '已出'),
    )
    show_choices = (
        (0, '未删除'),
        (1, '已经删除'),
    )

    content = models.CharField(max_length=500, default='', verbose_name='内容')
    price = models.IntegerField(verbose_name="价格",default=0)
    view_num = models.IntegerField(verbose_name="浏览量",default=0)
    good_num = models.IntegerField(verbose_name="点赞数",default=0)
    want_num = models.IntegerField(verbose_name="想要人数",default=0)
    report_num = models.IntegerField(verbose_name="举报数",default=0)
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否删除')
    create_date = models.DateField(auto_now_add=True, verbose_name="日期")
    create_time = models.TimeField(auto_now_add=True, verbose_name="时间")
    is_first = models.SmallIntegerField(default=0, choices=first_choices, verbose_name='置顶')
    is_type = models.SmallIntegerField(default=1, choices=type_choices, verbose_name='新型')
    is_sale = models.SmallIntegerField(default=0, choices=sale_choices, verbose_name='出售')

    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey('user.User',verbose_name='发布者',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_second'
        verbose_name = "校园二手·发布"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


# 二手市场 相关图片
class SecondImg(models.Model):
    qiniu_img = models.CharField(max_length=100, default='', verbose_name='七牛地址')
    local_img = models.ImageField(verbose_name='本地地址', upload_to='second/%Y/%m/%d', default='')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="日期时间")

    second = models.ForeignKey('Second', verbose_name='校园二手', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_second_img'
        verbose_name = "校园二手·图片"
        verbose_name_plural = verbose_name


# 二手市场 评论表
class SecondComment(models.Model):
    show_choices = (
        (0, '未删除'),
        (1, '已经删除'),
    )
    content = models.CharField(max_length=300,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="评论时间")
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否删除')
    replay_num = models.IntegerField(verbose_name="评论回复数量",default=0)

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    second = models.ForeignKey('Second', verbose_name='二手', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'dn_second_comment'
        verbose_name = "校园二手·评论"
        verbose_name_plural = verbose_name


# 二手市场 评论回复表 二级评论
class SecondReplyComment(models.Model):
    content = models.CharField(max_length=300,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="回复评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="回复评论时间")

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    second = models.ForeignKey('Second', verbose_name='二手', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('SecondComment', verbose_name='评论', on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', verbose_name='自关联的父级', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_second_comment_reply'
        verbose_name = "校园二手·评论回复"
        verbose_name_plural = verbose_name


# 二手市场 举报表
class SecondReport(models.Model):
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    second = models.ForeignKey('Second',verbose_name='二手id',on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='用户id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_second_report'
        verbose_name = "校园二手·举报"
        verbose_name_plural = verbose_name


# 屏蔽二手市场表
class RefuseSecond(models.Model):
    second = models.ForeignKey('Second',verbose_name='二手id',on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='用户id', on_delete=models.CASCADE, null=True)
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = 'dn_second_refuse'
        verbose_name = "校园二手·屏蔽"
        verbose_name_plural = verbose_name

