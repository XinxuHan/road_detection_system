from django import forms
from django.core.exceptions import ValidationError
import re
from .models import UserProfile

class RegisterForm(forms.Form):
    account = forms.CharField(
        min_length=1,
        max_length=50,
        error_messages={
            "required": "The account cannot be empty!",
            "min_length": "The account length must be between 1 and 11 characters",
            "max_length": "The account length must be between 1 and 11 characters",
        }
    )
    phone = forms.CharField(
        label="Contact number:",
        widget=forms.TextInput(attrs={
            "placeholder": "Please enter your contact number!",
            "size": 38,
        }),
        error_messages={"required": "The mobile phone number cannot be empty!"}
    )
    email = forms.EmailField(
        label="Email:",
        widget=forms.EmailInput(attrs={
            "placeholder": "Please enter your email address!",
            "size": 38,
        }),
        error_messages={
            "required": "The mailbox cannot be empty!",
            "invalid": "The email format is incorrect!",
        }
    )
    password = forms.CharField(
        label="Password:",
        min_length=6,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Please enter the password!",
            "size": 38,
        }),
        error_messages={
            "required": "The password cannot be empty!",
            "min_length": "The password must be at least 6 characters long.",
            "max_length": "The password must not exceed 50 characters."
        }
    )
    checkPassword = forms.CharField(
        label="Confirmation password:",
        min_length=6,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Please enter the confirmation password!",
            "size": 38,
        }),
        error_messages={
            "required": "Please enter the confirmation password!",
            "min_length": "The confirmation password must be at least 6 characters long.",
            "max_length": "The confirmation password must not exceed 50 characters."
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        pw, cpw = cleaned_data.get("password"), cleaned_data.get("checkPassword")
        if pw and cpw and pw != cpw:
            raise ValidationError("The passwords entered twice are inconsistent!")
        return cleaned_data

    def clean_account(self):
        account = self.cleaned_data.get("account")
        if not re.match(r'^[a-zA-Z0-9_]+$', account):
            raise ValidationError("The account can only contain letters, numbers and underscores, and cannot contain Chinese characters.")
        if UserProfile.objects.filter(account=account).exists():
            raise ValidationError("The account already exists!")
        return account

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("The email address already exists!")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if UserProfile.objects.filter(phone=phone).exists():
            raise ValidationError("The mobile phone number already exists!")
        return phone


class LoginForm(forms.Form):
    nick_name = forms.CharField(
        label="User name",
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={
            "placeholder": "Please enter the username!",
            "class": "validate-username",
            "size": 38,
            "maxlength": 99
        }),
        error_messages={
            "required": "The username cannot be empty!",
            "min_length": "The length of the username must be between 3 and 10 characters.",
            "max_length": "The length of the username must be between 3 and 10 characters."
        }
    )

    password = forms.CharField(
        label="Password",
        min_length=6,
        max_length=99,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Please enter the password!",
            "class": "validate-password",
            "size": 38,
            "maxlength": 99
        }),
        error_messages={
            "required": "The password cannot be empty!",
            "min_length": "The password must be at least 6 characters long.",
            "max_length": "The password must not exceed 50 characters."
        }
    )
