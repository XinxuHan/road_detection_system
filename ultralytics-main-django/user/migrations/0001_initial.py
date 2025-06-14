from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nick_name", models.CharField(blank=True, max_length=20, null=True)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("password", models.CharField(max_length=256, verbose_name="用户密码")),
                ("phone", models.CharField(blank=True, max_length=11, null=True)),
                (
                    "avatar",
                    models.ImageField(blank=True, null=True, upload_to="avatars/"),
                ),
                ("addtime", models.DateTimeField(auto_now_add=True)),
                ("pdated_at", models.DateTimeField(auto_now=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("1", "男"), ("0", "女")],
                        max_length=6,
                        null=True,
                        verbose_name="性别",
                    ),
                ),
                ("age", models.IntegerField(blank=True, null=True, verbose_name="年龄")),
                (
                    "account",
                    models.CharField(max_length=100, unique=True, verbose_name="账号"),
                ),
            ],
            options={
                "db_table": "user_profile",
            },
        ),
    ]
