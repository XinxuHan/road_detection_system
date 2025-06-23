from django.db import models

class UserProfile(models.Model):
    account = models.CharField(max_length=100, unique=True, verbose_name="account")
    password = models.CharField(max_length=256, verbose_name="password")
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    nick_name = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    gender = models.CharField(
        max_length=6,
        choices=[('1', 'male'), ('0', 'female')],
        null=True,
        blank=True,
        verbose_name="Gender"
    )
    age = models.IntegerField(null=True, blank=True, verbose_name="Age")
    addtime = models.DateTimeField(auto_now_add=True)
    pdated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.account
table = 'user_profile'