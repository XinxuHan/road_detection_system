from django.db import models



class UserProfile(models.Model):
    nick_name = models.CharField(max_length=20, null=True, blank=True)  # 用户昵称
    email = models.EmailField(max_length=100, unique=True)  # 邮箱,unique=True：确保该字段的值在数据库中是唯一的
    password = models.CharField(max_length=256, verbose_name="用户密码")
    phone = models.CharField(max_length=11, null=True,blank=True)  # 手机号
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # 用户头像
    addtime = models.DateTimeField(auto_now_add=True)   # 创建时间，自动记录创建时间
    pdated_at = models.DateTimeField(auto_now=True)     # 自动记录用户的最后一次更新时间
    gender = models.CharField(max_length=6,choices=[('1', '男'), ('0', '女')],null=True,blank=True,verbose_name="性别")
    age = models.IntegerField(null=True, blank=True, verbose_name="年龄")
    account = models.CharField(max_length=100, unique=True, verbose_name="账号")

    class Meta:
        db_table = 'user_profile'