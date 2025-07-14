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
        return JsonResponse({'error': 'Wrong account or password!'})

    request.session.update({
        'is_login': True,
        'user_id': user_profile.id,
        'account': user_profile.account,
    })

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
        'message': 'Login successfully',
        'user': user_info
    })


@api_view(['POST'])
def register_view(request):

    form = RegisterForm(request.data)

    if not form.is_valid():
        errors = {field: errors[0] for field, errors in form.errors.items()}
        return JsonResponse({
            'success': False,
            'errors': errors,
        })

    cleaned = form.cleaned_data
    user = UserProfile.objects.create(
        account=cleaned['account'],
        email=cleaned['email'],
        password=cleaned['password'],
        phone=cleaned['phone'],
        avatar='img.png', 
        nick_name=cleaned['account'],
    )

    return JsonResponse({
        'success': True,
        'message': 'Signup successfully',
    }, status=201)


@csrf_exempt
def update_user_view(request):

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    user_account = data.get('account')
    if not user_account:
        return JsonResponse({"error": "Account required"}, status=400)

    user_profile = UserProfile.objects.filter(account=user_account).first()
    if not user_profile:
        return JsonResponse({"error": "User not found"}, status=404)

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

    update_fields = {k: v for k, v in update_fields.items() if v is not None}

    for field, value in update_fields.items():
        setattr(user_profile, field, value)

    user_profile.save()

    return JsonResponse({"message": "Information update successfully"})

@csrf_exempt
@api_view(['POST'])
def upload_avatar_view(request):

    avatar_file = request.FILES.get('avatar')
    if not avatar_file:
        return JsonResponse({"error": "No avatar uploaded"}, status=400)

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f"{timestamp}-{avatar_file.name}"
    save_path = os.path.join(settings.USER_AVATAR_ROOT, file_name)

    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as destination:
            for chunk in avatar_file.chunks():
                destination.write(chunk)

        return JsonResponse({
            "message": "Avatar uploaded successfully",
            "avatarUrl": file_name
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Failed to upload: {str(e)}"
        }, status=500)



@api_view(['POST'])
def change_password_view(request):

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    old_password = data.get('old_password')
    new_password = data.get('new_password')
    email = data.get('email')

    if not all([old_password, new_password, email]):
        return JsonResponse({"error": "Required field is missing"}, status=400)

    user_profile = UserProfile.objects.filter(email=email).first()
    if not user_profile:
        return JsonResponse({"error": "Can't find the user"}, status=404)

    if user_profile.password != old_password:
        return JsonResponse({'code': '500', 'error': "Wrong original password！"})

    user_profile.password = new_password
    user_profile.save()

    return JsonResponse({'code': '200'})