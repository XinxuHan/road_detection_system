import re

from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile

class RegisterForm(forms.Form):
    account = forms.CharField(
        max_length=50,
        min_length=1,
        error_messages={
            "required": "账号不能为空！",
            "min_length": "账号长度必须在1到11位之间",
            "max_length": "账号长度必须在1到11位之间",
        }
    )
    phone = forms.CharField(
        label="联系电话 ：",
        widget=forms.TextInput(attrs={
            "placeholder": "请输入联系电话！",
            "size": "38",
        }),
        error_messages={
            "required": "手机号不能为空！",
        }
    )
    email = forms.EmailField(
        label="邮箱 ：",
        widget=forms.EmailInput(attrs={
            "placeholder": "请输入邮箱！",
            "size": "38",
        }),
        error_messages={
            "required": "邮箱不能为空！",
            "invalid": "邮箱格式不正确！",
        }
    )
    password = forms.CharField(
        label="密码 ：",
        widget=forms.PasswordInput(attrs={
            "placeholder": "请输入密码！",
            "size": "38",
        }),
        error_messages={
            "required": "密码不能为空！",
        }
    )
    checkPassword = forms.CharField(
        label="确认密码 ：",
        widget=forms.PasswordInput(attrs={
            "placeholder": "请输入确认密码！",
            "size": "38",
        }),
        error_messages={
            "required": "请输入确认密码！",
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        checkPassword = cleaned_data.get("checkPassword")

        if password and checkPassword and password != checkPassword:
            raise ValidationError("两次密码不一致！")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("邮箱已经存在！")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if UserProfile.objects.filter(phone=phone).exists():
            raise ValidationError("手机号已经存在！")
        return phone


    def clean_account(self):
        """
        检查账号是否已经存在，并验证账号格式
        """
        account = self.cleaned_data.get("account")

        # 验证账号格式：只能包含字母、数字和下划线，且不允许包含中文字符
        account_regex = re.compile(r'^[a-zA-Z0-9_]+$')
        if not account_regex.match(account):
            raise ValidationError("账号只能包含字母、数字和下划线，且不能包含中文字符")

        # 检查账号是否已经存在
        if UserProfile.objects.filter(account=account).exists():
            raise ValidationError("账号已存在！")

        return account




class LoginForm(forms.Form):
    """
    登录功能
    """
    nick_name = forms.CharField(
        label="用户名",
        max_length=50,
        min_length=3,
        widget=forms.TextInput(attrs={
            "placeholder": "请输入用户名！",
            "class": "validate-username",
            "size": 38,
            "maxlength": 99
        }),
        error_messages={
            "required": "用户名不能为空！",
            "max_length": "用户名长度必须在3到10位之间"
        }
    )

    password = forms.CharField(
        label="密码",
        max_length=99,
        widget=forms.PasswordInput(attrs={
            "placeholder": "请输入密码！",
            "class": "validate-password",
            "size": 38,
            "maxlength": 99
        }),
        error_messages={
            "required": "密码不能为空！",
            "max_length": "密码长度不少于6位"
        }
    )



