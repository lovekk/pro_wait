from django.db import models


# 帮助 help
class Help(models.Model):
    content = models.CharField(max_length=500, verbose_name="help内容", default="")
    publish_date = models.DateField(auto_now_add=True, verbose_name="发布日期")
    publish_time = models.TimeField(auto_now_add=True, verbose_name="发布时间")
    price = models.IntegerField(verbose_name="价格",default=0)
    report_num = models.IntegerField(verbose_name="举报数", default=0)
    view_num = models.IntegerField(verbose_name="浏览量", default=0)
    is_online = models.SmallIntegerField(default=0, choices=((0, '线上'),(1, '线下')), verbose_name='线上线下')
    is_all_school =  models.SmallIntegerField(default=0, choices=((0, '本校'),(1, '所有学校')), verbose_name='是否所有学校可见')
    is_show = models.SmallIntegerField(default=0, choices=((0, '未删除'),(1, '已经删除')), verbose_name='是否取消')
    status = models.SmallIntegerField(default=0, choices=((0, '未接单'), (1, '已接'), (2, '交易完成 ')), verbose_name='交易状态')
    finish_datetime = models.DateTimeField(auto_now=True, verbose_name="完成时间")

    school = models.ForeignKey('user.School', verbose_name='学校', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='发布人', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'dn_help'
        verbose_name = "help·发布内容"
        verbose_name_plural = verbose_name


# 帮助 接单表
class HelpOrder(models.Model):
    order_date = models.DateField(auto_now_add=True, verbose_name="接单日期")
    order_time = models.TimeField(auto_now_add=True, verbose_name="接单时间")
    is_you = models.SmallIntegerField(default=0, choices=((0, '是你'),(1, '不是你')), verbose_name='是不是你去完成')

    user = models.ForeignKey('user.User', verbose_name='接单者', on_delete=models.CASCADE, null=True)
    myhelp = models.ForeignKey('Help', verbose_name='help_id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_help_order'
        verbose_name = "help·接单"
        verbose_name_plural = verbose_name


# 帮助 图片表
class HelpImage(models.Model):
    qiniu_img = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_img = models.ImageField(verbose_name="本地地址",upload_to='myhelp/%Y/%m/%d',default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    myhelp = models.ForeignKey('Help', verbose_name='help_id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_help_image'
        verbose_name = "help·图片"
        verbose_name_plural = verbose_name


# 帮助 评论表
class HelpComment(models.Model):
    show_choices = (
        (0, '未删除'),
        (1, '已经删除'),
    )
    content = models.CharField(max_length=300,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="评论时间")
    is_show = models.SmallIntegerField(default=0, choices=show_choices, verbose_name='是否显示')

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    myhelp = models.ForeignKey('Help', verbose_name='help_id', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'dn_help_comment'
        verbose_name = "help·评论"
        verbose_name_plural = verbose_name


# 帮助 评论 图片表
class HelpCommentImage(models.Model):
    qiniu_img = models.CharField(max_length=100, verbose_name="七牛云地址", default="")
    local_img = models.ImageField(verbose_name="本地地址", upload_to='myhelp_comment_img/%Y/%m/%d', default="")
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    comment = models.ForeignKey('HelpComment', verbose_name='评论id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_help_comment_image'
        verbose_name = "Help·评论·图片"
        verbose_name_plural = verbose_name


# 帮助 评论回复表 二级评论
class HelpReplyComment(models.Model):

    content = models.CharField(max_length=300,verbose_name="评论内容",default="")
    comment_date = models.DateField(auto_now_add=True, verbose_name="回复评论日期")
    comment_time = models.TimeField(auto_now_add=True, verbose_name="回复评论时间")

    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    myhelp = models.ForeignKey('Help', verbose_name='help_id', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('HelpComment', verbose_name='评论', on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', verbose_name='自关联的父级', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_help_comment_reply'
        verbose_name = "Help·评论·回复"
        verbose_name_plural = verbose_name


# 帮助 举报表
class HelpReport(models.Model):
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    myhelp = models.ForeignKey('Help',verbose_name='help_id',on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='用户id', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_help_report'
        verbose_name = "help·举报"
        verbose_name_plural = verbose_name


# 屏蔽help表
# help也有屏蔽用户 用户表在moment中
class RefuseHelp(models.Model):
    myhelp = models.ForeignKey('Help',verbose_name='help_id',on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('user.User', verbose_name='用户id', on_delete=models.CASCADE, null=True)
    publish_datetime = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = 'dn_help_refuse'
        verbose_name = "help·屏蔽"
        verbose_name_plural = verbose_name

