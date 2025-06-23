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
                        verbose_name="ID"
                    ),
                ),
                ("account", models.CharField(max_length=100, unique=True, verbose_name="account")),
                ("password", models.CharField(max_length=256, verbose_name="password")),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone", models.CharField(max_length=20, null=True, blank=True)),
                ("nick_name", models.CharField(max_length=20, null=True, blank=True)),
                (
                    "gender",
                    models.CharField(
                        max_length=6,
                        choices=[("1", "male"), ("0", "female")],
                        null=True,
                        blank=True,
                        verbose_name="Gender"
                    ),
                ),
                ("age", models.IntegerField(null=True, blank=True, verbose_name="age")),
                ("avatar", models.ImageField(upload_to="avatars/", null=True, blank=True)),
                ("addtime", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "user_profile",
            },
        ),
    ]
