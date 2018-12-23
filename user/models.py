from django.db import models
from datetime import datetime

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

    token = models.CharField(max_length=100,verbose_name='身份令牌',default="")
    device_num = models.CharField(max_length=100,verbose_name='设备唯一标识',default="")
    device_model = models.CharField(max_length=100,verbose_name='设备型号',default="")
    device_name = models.CharField(max_length=100,verbose_name='设备名称',default="")
    operator = models.CharField(max_length=100,verbose_name='设备运营商名称',default="")
    create_date = models.DateTimeField(default=datetime.now, verbose_name="注册时间")
    integral = models.IntegerField(verbose_name='积分',default=0)

    is_delete = models.SmallIntegerField(default=0, choices=delete_choices, verbose_name='销户')
    is_school_auth = models.SmallIntegerField(default=0, choices=school_auth_choices, verbose_name='学生认证')
    is_real_name_auth = models.SmallIntegerField(default=0, choices=real_name_auth_choices, verbose_name='实名认证')
    is_official_auth = models.SmallIntegerField(default=0, choices=official_auth_choices, verbose_name='官方认证')
    is_alipay_auth = models.SmallIntegerField(default=0, choices=alipay_auth_choices, verbose_name='支付宝认证')


    class Meta:
        db_table = 'dn_user'
        verbose_name = "用户信息"
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
        verbose_name = '学校信息'
        verbose_name_plural = verbose_name


# 关注用户
class Follow(models.Model):
    follow_id = models.IntegerField(verbose_name='我的关注用户id',default=0)
    create_date = models.DateField(auto_now_add=True,verbose_name="创建日期")
    create_time = models.TimeField(auto_now_add=True,verbose_name="创建时间")
    user = models.ForeignKey('user.User',verbose_name='用户',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_user_follow'
        verbose_name = "用户关注"
        verbose_name_plural = verbose_name


# 学校模块
class FunctionModule(models.Model):
    module_name = models.CharField(max_length=30, default='', verbose_name='学校名称')
    create_datetime = models.DateTimeField(auto_now_add=True,verbose_name="创建日期")
    school = models.ForeignKey('user.School',verbose_name='学校',on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'dn_school_module'
        verbose_name = "学校模块"
        verbose_name_plural = verbose_name
