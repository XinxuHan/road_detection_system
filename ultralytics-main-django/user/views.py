import datetime
import json
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from YOLOv11 import settings
from .forms import RegisterForm
from .models import UserProfile
from django.http import JsonResponse

@api_view(['POST'])
def login_view(request):

    data = request.data
    account = data.get('account')
    password = data.get('password')

    user_profile = UserProfile.objects.filter(account=account).first()
    if not user_profile or user_profile.password != password:
        return JsonResponse({'error': '错误的账号或密码！'})

    # 设置 session 信息
    request.session.update({
        'is_login': True,
        'user_id': user_profile.id,
        'account': user_profile.account,
    })

    # 构造用户信息
    user_info = {
        'id': user_profile.id,
        'account': user_profile.account,
        'nick_name': user_profile.nick_name,
        'avatar': user_profile.avatar.name if user_profile.avatar else None,
        'email': user_profile.email,
        'phone': user_profile.phone,
        'gender': user_profile.gender,
        'age': user_profile.age,
        'addtime': user_profile.addtime,
    }

    return JsonResponse({
        'success': True,
        'message': '登录成功',
        'user': user_info
    })


@api_view(['POST'])
def register_view(request):

    form = RegisterForm(request.data)

    if not form.is_valid():
        # 返回验证失败的第一个错误信息
        errors = {field: errors[0] for field, errors in form.errors.items()}
        return JsonResponse({
            'success': False,
            'errors': errors,
        })

    # 提取表单数据
    cleaned = form.cleaned_data
    user = UserProfile.objects.create(
        account=cleaned['account'],
        email=cleaned['email'],
        password=cleaned['password'],
        phone=cleaned['phone'],
        avatar='img.png',  # 默认头像
        nick_name=cleaned['account'],
    )

    return JsonResponse({
        'success': True,
        'message': '注册成功',
    }, status=201)


@csrf_exempt
def update_user_view(request):

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "无效的 JSON 格式"}, status=400)

    user_email = data.get('email')
    if not user_email:
        return JsonResponse({"error": "缺少 email 字段"}, status=400)

    user_profile = UserProfile.objects.filter(email=user_email).first()
    if not user_profile:
        return JsonResponse({"error": "未找到该邮箱对应的用户"}, status=404)

    def handle_null(value):
        return None if value == "null" else value

    update_fields = {
        'nick_name': data.get('nick_name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'age': handle_null(data.get('age')),
        'gender': data.get('gender'),
    }

    if 'avatar' in data:
        avatar_url = data['avatar']
        update_fields['avatar'] = os.path.basename(avatar_url)

    # 去除值为 None 的字段，避免不必要的更新
    update_fields = {k: v for k, v in update_fields.items() if v is not None}

    for field, value in update_fields.items():
        setattr(user_profile, field, value)

    user_profile.save()

    return JsonResponse({"message": "用户信息更新成功!"})

@csrf_exempt
@api_view(['POST'])
def upload_avatar_view(request):

    avatar_file = request.FILES.get('avatar')
    if not avatar_file:
        return JsonResponse({"error": "未上传头像"}, status=400)

    # 构建文件名与保存路径
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f"{timestamp}-{avatar_file.name}"
    save_path = os.path.join(settings.USER_AVATAR_ROOT, file_name)

    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as destination:
            for chunk in avatar_file.chunks():
                destination.write(chunk)

        return JsonResponse({
            "message": "头像上传成功",
            "avatarUrl": file_name
        })

    except Exception as e:
        return JsonResponse({
            "error": f"上传失败: {str(e)}"
        }, status=500)



@api_view(['POST'])
def change_password_view(request):

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "无效的 JSON 数据"}, status=400)

    old_password = data.get('old_password')
    new_password = data.get('new_password')
    email = data.get('email')

    if not all([old_password, new_password, email]):
        return JsonResponse({"error": "缺少必要字段"}, status=400)

    user_profile = UserProfile.objects.filter(email=email).first()
    if not user_profile:
        return JsonResponse({"error": "未找到该用户"}, status=404)

    if user_profile.password != old_password:
        return JsonResponse({'code': '500', 'error': "原密码错误！"})

    # 更新密码
    user_profile.password = new_password
    user_profile.save()

    return JsonResponse({'code': '200'})