from django.urls import path, re_path
from django.views.static import serve as static_serve
from YOLOv11 import settings
from . import views as user_views

# User interface routing collection
user_urlpatterns = [
    path('api/login/', user_views.login_view, name='longin'),
    path('api/register/', user_views.register_view, name='register'),
    path('api/update_user/', user_views.update_user_view, name='update_user'),
    path('api/upload-avatar/', user_views.upload_avatar, name='upload_avatar'),
    path('api/update_password/', user_views.change_password, name='change_password'),
]

# Static resource access (user avatar)
media_serve_url = re_path(
    r'^user/media/avatar(?P<path>.*)$',
    static_serve,
    {'document_root': settings.USER_AVATAR_ROOT}
)

# Summarize all routes
urlpatterns = user_urlpatterns + [media_serve_url]
