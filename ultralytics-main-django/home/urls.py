from django.contrib import admin
from django.urls import path
from home import views  # 导入视图函数
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from . import consumers
from home.views import analyze_llm_view

urlpatterns = [
    path('detect/', views.detect_view, name='detect'),
    path('api/set_model/', views.set_model_view, name='set_model'),
    path("api/set_model_params/", views.set_confidence_view, name="set_confidence"),
    path("api/upload-video/", views.upload_video, name="upload_video"),
    path("api/get-frame/", views.get_frame, name="get_frame"),
    path("api/stop_detection/", views.stop_detection, name="stop_detection"),
    path('api/start-camera', views.start_camera),  # 摄像头接口
    path("api/get-latest-frame/", views.get_latest_frame, name="get_latest_frame"),
    path('api/analyze-llm/', views.analyze_llm_view, name='analyze_llm'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 访问媒体文件
