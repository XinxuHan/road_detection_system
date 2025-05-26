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
    """
    用户登录
    """
    account = request.data.get('account')
    password = request.data.get('password')


    try:
        user_profile = UserProfile.objects.get(account=account)  # 根据 account 查找账号
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': '错误的账号或密码！'})


    if user_profile.password == password:  # 使用明文密码比较
        request.session['is_login'] = True
        request.session['user_id'] = user_profile.id
        request.session['account'] = user_profile.account

        return JsonResponse({
            'success': True,
            'message': '登录成功',
            'user': {
                'id': user_profile.id,
                'account': user_profile.account,
                'nick_name': user_profile.nick_name,
                # 拼接正确的头像URL
                'avatar': user_profile.avatar.name if user_profile.avatar else None,
                'email': user_profile.email,
                'phone': user_profile.phone,
                'gender': user_profile.gender,
                'age': user_profile.age,
                'addtime': user_profile.addtime,
            }
        })
    else:
        return JsonResponse({'error': '错误的账号或密码！'})


@api_view(['POST'])
def register_view(request):
    """
    用户注册视图
    """
    form = RegisterForm(request.data)

    if form.is_valid():
        # 表单验证通过
        account = form.cleaned_data['account']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        phone = form.cleaned_data['phone']
        avatar = 'img.png'  # 默认头像

        new_user = UserProfile(
            account=account,
            email=email,
            password=password,
            phone=phone,
            avatar=avatar,
            nick_name=account
        )
        new_user.save()

        return JsonResponse({
            'success': True,
            'message': '注册成功',
        }, status=201)
    else:
        # 表单验证失败，返回错误信息
        errors = {field: error_list[0] for field, error_list in form.errors.items()}
        return JsonResponse({
            'success': False,
            'errors': errors,
        })



@csrf_exempt
def update_user_view(request):
    """
    用户信息更新接口
    """
    data = json.loads(request.body.decode("utf-8"))
    #print(data)

    # 此处使用 email 来获取用户
    user_email = data.get('email')
    if not user_email:
        return JsonResponse({"error": "缺少 email 字段"})

    try:
        # 查找现有的用户，如果没有找到则返回错误
        user_profile = UserProfile.objects.get(email=user_email)
        updated_data = {}


        def handle_null(value):
            return None if value == "null" else value


        if 'nick_name' in data:
            updated_data['nick_name'] = data['nick_name']
        if 'email' in data:
            updated_data['email'] = data['email']
        if 'phone' in data:
            updated_data['phone'] = data['phone']
        if 'age' in data:
            updated_data['age'] = handle_null(data['age'])
        if 'gender' in data:
            updated_data['gender'] = data['gender']
        if 'avatar' in data:
            avatar_url = data['avatar']
            avatar_filename = os.path.basename(avatar_url)
            updated_data['avatar'] = avatar_filename


        for field, value in updated_data.items():
            setattr(user_profile, field, value)

        user_profile.save()

        return JsonResponse({"message": "用户信息更新成功!"})

    except Exception as e:
        return JsonResponse({"error": str(e)})


@csrf_exempt
@api_view(['POST'])
def upload_avatar(request):
    avatar = request.FILES.get('avatar')  # 获取上传的头像文件
    if not avatar:
        return JsonResponse({"error": "未上传头像"})

    # 保存头像文件
    try:
        new_file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + avatar.name
        avatar_path = os.path.join(settings.USER_AVATAR_ROOT, new_file_name)
        os.makedirs(os.path.dirname(avatar_path), exist_ok=True)

        # 保存文件到服务器
        with open(avatar_path, 'wb') as f:
            for chunk in avatar.chunks():
                f.write(chunk)

        return JsonResponse({"message": "头像上传成功", "avatarUrl": new_file_name})
    except:
        return JsonResponse({"error": "上传失败"})




@api_view(['POST'])
def change_password(request):
    """
    修改密码接口
    """
    data = json.loads(request.body.decode("utf-8"))
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    email = data.get('email')

    try:
        user_profile = UserProfile.objects.get(email=email)
        if user_profile.password == old_password:
            # 更新密码
            user_profile.password = new_password
            user_profile.save()
            return JsonResponse({'code': '200'})
        else:
            return JsonResponse({'code': '500',  'error': "原密码错误！"})

    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "未找到该用户"})
    except Exception as e:
        return JsonResponse({"error": str(e)})