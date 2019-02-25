from django.db import models
from datetime import datetime
from tinymce.models import HTMLField

# 用户信息
class User(models.Model):
    delete_choices = (
        (0, '正常'),
        (1, '已销户'),
    )
    school_auth_choices = (
        (0, '未认证'),
        (1, '已认证'),
    )
    real_name_auth_choices = (
        (0, '未认证'),
        (1, '已认证'),
    )
    official_auth_choices = (
        (0, '未认证'),
        (1, '已认证'),
    )
    alipay_auth_choices = (
        (0, '未认证'),
        (1, '已认证'),
    )

    phone_num = models.CharField(max_length=15,verbose_name="手机号", default="")
    password = models.CharField(max_length=50,verbose_name='密码')

    nick = models.CharField(max_length=30,verbose_name="昵称", default="")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female",verbose_name="性别")
    head_image = models.ImageField(verbose_name="用户头像", upload_to="user/%Y/%m/%d", default="")
    head_qn_url = models.CharField(max_length=100,verbose_name='七牛头像地址', default="")
    account_num = models.CharField(max_length=10,verbose_name='等号', default="")
    my_sign = models.CharField(max_length=128,verbose_name='个性签名', default="")

    birthday = models.DateField(verbose_name="出生日期", blank=True, null=True)
    real_name = models.CharField(max_length=30,verbose_name='真实姓名',default="")
    id_card_num = models.CharField(max_length=20,verbose_name='身份证号',default="")

    school = models.ForeignKey('School',verbose_name='学校id',on_delete=models.CASCADE,null=True)

    school_name = models.CharField(max_length=30,verbose_name='学校',default="")
    college_name = models.CharField(max_length=30,verbose_name='学院',default="")
    major = models.CharField(max_length=30,verbose_name='专业',default="")
    stu_num = models.CharField(max_length=30,verbose_name='学号',default="")
    stu_password = models.CharField(max_length=30,verbose_name='学号密码',default="")

    reg_ip = models.CharField(max_length=100, default='', verbose_name='注册IP')
    token = models.CharField(max_length=100,verbose_name='身份令牌',default="")
    device_num = models.CharField(max_length=50,verbose_name='设备唯一标识',default="")
    device_model = models.CharField(max_length=50,verbose_name='设备型号',default="")
    device_name = models.CharField(max_length=30,verbose_name='设备名称',default="")
    operator = models.CharField(max_length=30,verbose_name='设备运营商名称',default="")
    system_type = models.CharField(max_length=30,verbose_name='手机系统类型',default="")
    channel = models.CharField(max_length=50, verbose_name='下载渠道来源', default="")
    create_date = models.DateTimeField(default=datetime.now, verbose_name="注册时间")
    integral = models.IntegerField(verbose_name='积分',default=0)

    good_total = models.IntegerField(verbose_name="获喜欢总数", default=0)
    comment_total = models.IntegerField(verbose_name="获评论总数", default=0)
    fans_total = models.IntegerField(verbose_name="获粉丝总数", default=0)
    create_total = models.IntegerField(verbose_name="获关注总数", default=0)
    find_total = models.IntegerField(verbose_name="说说总数", default=0)
    help_total = models.IntegerField(verbose_name="help总数", default=0)

    is_delete = models.SmallIntegerField(default=0, choices=delete_choices, verbose_name='销户')
    is_school_auth = models.SmallIntegerField(default=0, choices=school_auth_choices, verbose_name='学生认证')
    is_real_name_auth = models.SmallIntegerField(default=0, choices=real_name_auth_choices, verbose_name='实名认证')
    is_official_auth = models.SmallIntegerField(default=0, choices=official_auth_choices, verbose_name='官方认证')
    is_alipay_auth = models.SmallIntegerField(default=0, choices=alipay_auth_choices, verbose_name='支付宝认证')

    class Meta:
        db_table = 'dn_user'
        verbose_name = "用户·账号资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nick


# 学校信息
class School(models.Model):
    enter_choices = (
        (0, '未入驻'),
        (1, '已入驻'),
    )
    name = models.CharField(max_length=30,default='',verbose_name='学校名称')
    province = models.CharField(max_length=20,default='',verbose_name='学校省')
    city = models.CharField(max_length=20,default='',verbose_name='学校市')
    is_show = models.BooleanField(default=False, verbose_name='是否显示在APP')
    is_enter = models.SmallIntegerField(default=0, choices=enter_choices, verbose_name='入驻')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dn_school'
        verbose_name = '学校列表'
        verbose_name_plural = verbose_name


# 关注用户
class Follow(models.Model):
    delete_choices = (
        (0, '关注中...'),
        (1, '已取消关注'),
    )
    follow_id = models.IntegerField(verbose_name='我的关注用户id',default=0)
    create_date = models.DateField(auto_now_add=True,verbose_name="创建日期")
    create_time = models.TimeField(auto_now_add=True,verbose_name="创建时间")
    is_delete = models.SmallIntegerField(default=0, choices=delete_choices, verbose_name='是否取消关注')
    user = models.ForeignKey('user.User',verbose_name='用户',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_user_follow'
        verbose_name = "用户·关注"
        verbose_name_plural = verbose_name


# 学校模块
class FunctionModule(models.Model):
    module_name = models.CharField(max_length=30, default='', verbose_name='模块名称')
    create_datetime = models.DateTimeField(auto_now_add=True,verbose_name="创建日期")
    school = models.ForeignKey('user.School',verbose_name='学校',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_school_module'
        verbose_name = "学校模块"
        verbose_name_plural = verbose_name


# 关于我们表
class AboutWe(models.Model):
    title = models.CharField(max_length=50, verbose_name="关于我们标题", default="")
    content = HTMLField(verbose_name="关于我们内容")
    create_date = models.DateField(auto_now_add=True, verbose_name="创建日期")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'dn_user_about'
        verbose_name = "关于我们"
        verbose_name_plural = verbose_name


# 关于我们评论表
class AboutWeComment(models.Model):
    delete_choices = (
        (0, '显示'),
        (1, '已删除'),
    )
    comment = models.CharField(max_length=120,default='', verbose_name='评论内容')
    create_date = models.DateField(auto_now_add=True, verbose_name="评论日期")
    create_time = models.TimeField(auto_now_add=True, verbose_name="评论日期")
    is_delete = models.SmallIntegerField(default=0, choices=delete_choices, verbose_name='是否显示')

    user = models.ForeignKey('User',verbose_name='用户',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_user_about_comment'
        verbose_name = "关于我们·评论"
        verbose_name_plural = verbose_name




# 回收人员表
class RecoveryPerson(models.Model):
    use_choices = (
        (0, '正在使用中...'),
        (1, '暂停使用'),
    )
    log_num = models.CharField(max_length=11, default='', verbose_name='登录账户')
    password = models.CharField(max_length=50,verbose_name='密码')
    is_use = models.SmallIntegerField(default=0, choices=use_choices, verbose_name='账号状态是否开放')

    school = models.ForeignKey('School',verbose_name='学校',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_user_recovery_worker'
        verbose_name = "用户·回收人员"
        verbose_name_plural = verbose_name



# 登录表
class Login(models.Model):
    phone_num = models.CharField(max_length=15, verbose_name="手机号", default="")
    password = models.CharField(max_length=50, verbose_name='密码', default="")
    log_ip = models.CharField(max_length=100,  verbose_name='登录IP', default="")
    device_num = models.CharField(max_length=50, verbose_name='设备唯一标识', default="")
    device_model = models.CharField(max_length=50, verbose_name='设备型号', default="")
    device_name = models.CharField(max_length=50, verbose_name='设备名称', default="")
    operator = models.CharField(max_length=50, verbose_name='设备运营商名称', default="")
    system_type = models.CharField(max_length=30, verbose_name='手机系统类型', default="")
    system_version = models.CharField(max_length=30, verbose_name='手机平台系统版本', default="")
    connection_type = models.CharField(max_length=30, verbose_name='网络连接类型', default="")
    screen_width = models.CharField(max_length=30, verbose_name='屏幕分辨率宽', default="")
    screen_height = models.CharField(max_length=30, verbose_name='屏幕分辨率高', default="")
    channel = models.CharField(max_length=50, verbose_name='下载渠道来源', default="")
    jail_break = models.CharField(max_length=10, verbose_name='设备是否越狱', default="")
    create_datetime = models.DateTimeField(auto_now_add=True,verbose_name="创建日期")

    user = models.ForeignKey('User', verbose_name='用户', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_user_login'
        verbose_name = "用户·登录"
        verbose_name_plural = verbose_name


# 积分商城 2019/2/19
class IntegralGoods(models.Model):
    name = models.CharField(max_length=10, verbose_name="商品名称", default="")
    price = models.IntegerField(verbose_name="商品价格", default="100")
    desc = models.CharField(max_length=200, verbose_name="商品描述", default="")
    image = models.ImageField(verbose_name="商品图片", upload_to="user_shop/%Y/%m/%d", default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dn_user_shop'
        verbose_name = "用户·积分商城"
        verbose_name_plural = verbose_name


# 订单表  2019/2/19
class IntegralOrder(models.Model):
    status_choice = (
        (0, '未发货'),
        (1, '已经发货'),
    )
    phone_num = models.CharField(max_length=15, verbose_name="手机号", default="")
    address = models.CharField(max_length=50,verbose_name="收货地址",default="")
    create_date = models.DateField(auto_now_add=True, verbose_name="订单时间")
    change_date = models.DateField(auto_now=True, verbose_name="修改时间")
    status = models.SmallIntegerField(default=0, choices=status_choice, verbose_name='是否发货')
    which_school = models.CharField(max_length=30, verbose_name="学校", default="")

    user = models.ForeignKey('User', verbose_name='收货人', on_delete=models.CASCADE, null=True)
    good = models.ForeignKey('IntegralGoods',verbose_name='商品', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_user_shop_order'
        verbose_name = "用户·积分订单"
        verbose_name_plural = verbose_name


# 成绩表
class Cj(models.Model):
    daima = models.CharField(max_length=50, verbose_name='课程编码')
    xueqi = models.CharField(max_length=50, verbose_name='学期')
    name = models.CharField(max_length=50,verbose_name='课程名字')
    number = models.CharField( max_length=20,verbose_name='分数')
    is_pass = models.CharField(max_length=50,verbose_name='是否通过')
    xuefen = models.CharField(max_length=50,verbose_name='学分')
    leibie = models.CharField(max_length=50,verbose_name='课程类别')

    user = models.ForeignKey('User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    school = models.ForeignKey('School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_user_score'
        verbose_name = "用户·成绩"
        verbose_name_plural = verbose_name


# 课表
class Kb(models.Model):
    yi1 = models.CharField(max_length=100)
    yi2 = models.CharField(max_length=100)
    yi3 = models.CharField(max_length=100)
    yi4 = models.CharField(max_length=100)
    yi5 = models.CharField(max_length=100)
    yi6 = models.CharField(max_length=100)
    yi7 = models.CharField(max_length=100)
    er1 = models.CharField(max_length=100)
    er2 = models.CharField(max_length=100)
    er3 = models.CharField(max_length=100)
    er4 = models.CharField(max_length=100)
    er5 = models.CharField(max_length=100)
    er6 = models.CharField(max_length=100)
    er7 = models.CharField(max_length=100)
    san1 = models.CharField(max_length=100)
    san2 = models.CharField(max_length=100)
    san3 = models.CharField(max_length=100)
    san4 = models.CharField(max_length=100)
    san5 = models.CharField(max_length=100)
    san6 = models.CharField(max_length=100)
    san7 = models.CharField(max_length=100)
    si1 = models.CharField(max_length=100)
    si2 = models.CharField(max_length=100)
    si3 = models.CharField(max_length=100)
    si4 = models.CharField(max_length=100)
    si5 = models.CharField(max_length=100)
    si6 = models.CharField(max_length=100)
    si7 = models.CharField(max_length=100)
    wu1 = models.CharField(max_length=100)
    wu2 = models.CharField(max_length=100)
    wu3 = models.CharField(max_length=100)
    wu4 = models.CharField(max_length=100)
    wu5 = models.CharField(max_length=100)
    wu6 = models.CharField(max_length=100)
    wu7 = models.CharField(max_length=100)

    user = models.ForeignKey('User', verbose_name='用户', on_delete=models.CASCADE, null=True)
    school = models.ForeignKey('School', verbose_name='学校', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'dn_user_class'
        verbose_name = "用户·课表"
        verbose_name_plural = verbose_name

