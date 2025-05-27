from django.urls import path,re_path
from django.views.static import serve

from YOLOv11 import settings
from . import views

urlpatterns = [
    path('api/login/', views.login_view, name='longin'),
    path('api/register/', views.register_view, name='register'),
    re_path(r'^user/media/avatar(?P<path>.*)$', serve, {'document_root': settings.USER_AVATAR_ROOT}),
    path('api/update_user/', views.update_user_view, name='update_user'),
    path('api/upload-avatar/', views.upload_avatar, name='upload_avatar'),  # 头像上传接口路由
    path('api/update_password/', views.change_password, name='change_password'),  # 修改密码接口

]
