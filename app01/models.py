from django.db import models


# Create your models here.
class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)

    # django中对输入进行约束
    gender_choice = (
        (1, '男'),
        (2, '女')
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")
    # 外键约束
    # on_delete
    # models.CASCADE 级联删除
    # 置空
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.SET_NULL,
                               null=True, blank=True)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name="价格",default=0)
    level_choices = {
        (1, "钻石")
        , (2, "黄金")
        , (3, "白银")
        , (4, "青铜")
        , (5, "黑铁")
    }

    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=5)

    status_choice = (
        (1, "已使用")
        , (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, default=2)
