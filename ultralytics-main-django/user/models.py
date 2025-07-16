from django.db import models


class UserData(models.Model):
    account = models.CharField(max_length=256, unique=True, verbose_name="account")
    password = models.CharField(max_length=256, verbose_name="password")
    email = models.EmailField(max_length=256, unique=True)
    phone = models.CharField(max_length=16, null=True, blank=True)
    name = models.CharField(max_length=32, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    gender = models.CharField(
        max_length=16,
        choices=[('1', 'male'), ('0', 'female')],
        null=True,
        blank=True,
        verbose_name="Gender"
    )
    age = models.IntegerField(null=True, blank=True, verbose_name="Age")
    add_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_data'

    def __str__(self):
        return self.account


table = 'user_data'
