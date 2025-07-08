from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from home import views as home_views
from home.views import analyze_llm_view


# Route list definition
api_routes = [
    path('detect/', home_views.recognition_view, name='detect'),
    path('api/set_model/', home_views.set_model_view, name='set_model'),
    path('api/set_model_params/', home_views.set_confidence_view, name='set_confidence'),
    path('api/upload-video/', home_views.upload_video_view, name='upload_video'),
    path('api/get-frame/', home_views.get_frame_view, name='get_frame'),
    path('api/stop_detection/', home_views.stop_recognition_view, name='stop_detection'),
    path('api/start-camera', home_views.start_camera_view),
    path('api/get-latest-frame/', home_views.get_latest_frame_view, name='get_latest_frame'),
    path('api/analyze-llm/', analyze_llm_view, name='analyze_llm'),
]

# Static resource mapping and API routing merging
urlpatterns = api_routes + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
