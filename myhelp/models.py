from django.db import models


class Help(models.Model):
    content = models.CharField(max_length=500, verbose_name="help内容", default="")
    publish_date = models.DateField(auto_now_add=True, verbose_name="发布日期")
    publish_time = models.TimeField(auto_now_add=True, verbose_name="发布时间")
    price = models.IntegerField(verbose_name="价格",default=0)
    report_num = models.IntegerField(verbose_name="举报数", default=0)
    is_online = models.SmallIntegerField(default=0, choices=((0, '线上'),(1, '线下')), verbose_name='线上线下')
    is_all_school =  models.SmallIntegerField(default=0, choices=((0, '本校'),(1, '所有学校')), verbose_name='是否所有学校可见')
    is_show = models.SmallIntegerField(default=0, choices=((0, '未删除'),(1, '已经删除')), verbose_name='是否取消')
    status = models.SmallIntegerField(default=0, choices=((0, '未接单'), (1, '已接单'), (2, '交易完成 ')), verbose_name='交易状态')
    finish_datetime = models.DateTimeField(auto_now=True, verbose_name="完成时间")

    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='发布人', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'dn_help'
        verbose_name = "help·发布内容"
        verbose_name_plural = verbose_name


# 接单表
class HelpOrder(models.Model):

    order_date = models.DateField(auto_now_add=True, verbose_name="接单日期")
    order_time = models.TimeField(auto_now_add=True, verbose_name="接单时间")
    is_you = models.SmallIntegerField(default=0, choices=((0, '是你'),(1, '不是你')), verbose_name='是不是你去完成')

    user = models.ForeignKey('user.User', verbose_name='接单者', on_delete=models.CASCADE, null=True)
    myhelp = models.ForeignKey('Help', verbose_name='Help id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_help_order'
        verbose_name = "help·接单"
        verbose_name_plural = verbose_name


# 图片表
class HelpImage(models.Model):
    qiniu_img = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_img = models.ImageField(verbose_name="本地地址",upload_to='myhelp/%Y/%m/%d',default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    myhelp = models.ForeignKey('Help', verbose_name='Help_id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_help_image'
        verbose_name = "help·图片"
        verbose_name_plural = verbose_name


# 评论表
class HelpComment(models.Model):
    show_choices = (
        (0, '未删除'),
        (1, '已经删除'),
    )
    content = models.CharField(max_length=100,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="评论时间")
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否删除')

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    myhelp = models.ForeignKey('Help', verbose_name='Help_id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_help_comment'
        verbose_name = "help·评论"
        verbose_name_plural = verbose_name

# 举报表
class HelpReport(models.Model):
    myhelp = models.ForeignKey('Help',verbose_name='Help_id',on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='用户id', on_delete=models.CASCADE, null=True)
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = 'dn_help_report'
        verbose_name = "help·举报"
        verbose_name_plural = verbose_name