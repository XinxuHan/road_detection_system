import json
import os
import threading
from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

from home.predict_img import detect
from home.predict_video_stream import process_video, frame_storage, process_camera

@csrf_exempt
def detect_view(request):
    if request.method == 'POST':
        input_image = request.FILES.get('content_image')
        if input_image:
            fs = FileSystemStorage()
            # 保存上传文件
            input_image_filename = fs.save(input_image.name, input_image)
            input_image_path = fs.path(input_image_filename)
            detection_result = detect(input_image_path)

            response_data = {
                'image_url': detection_result['image_url'],
                'results': detection_result['results']
            }


            return JsonResponse(response_data)

        else:
            return JsonResponse({'error': 'Content image not provided.'}, status=400)

    return JsonResponse({'error': '无效的请求方法'}, status=405)





@csrf_exempt
def upload_video(request):
    if request.method == "POST":
        video_file = request.FILES.get("video")
        if not video_file:
            return JsonResponse({"error": "No video uploaded"}, status=400)

        video_path = os.path.join(settings.MEDIA_ROOT, "uploaded_video.mp4")
        with open(video_path, "wb") as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        # 启动YOLO检测线程
        thread = threading.Thread(target=process_video, args=(video_path,))
        thread.start()

        return JsonResponse({"message": "视频上传成功"})



@csrf_exempt
def start_camera(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            camera_index = int(data.get("camera_index", 0))

            # 停止正在进行的检测
            with frame_storage["lock"]:
                if frame_storage["processing"]:
                    frame_storage["abort"] = True

            # 启动摄像头检测线程
            thread = threading.Thread(target=process_camera, args=(camera_index,))
            thread .start()

            return JsonResponse({
                "message": f"摄像头{camera_index}检测已启动",
                "camera_index": camera_index
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)






def get_frame(request):
    with frame_storage["lock"]:
        current_frame = frame_storage["latest_frame"]
        current_id = frame_storage["frame_id"]
        processing = frame_storage["processing"]
        detections = frame_storage["detections"]

    if not current_frame:
        return JsonResponse({
            "frame_url": None,
            "frame_id": 0,
            "processing": processing,
            "detections": []
        })

    import base64
    frame_base64 = base64.b64encode(current_frame).decode("utf-8")
    frame_url = f"data:image/jpeg;base64,{frame_base64}"

    return JsonResponse({
        "frame_url": frame_url,
        "frame_id": current_id,
        "processing": processing,
        "detections": detections
    })




def get_latest_frame(request):
    with frame_storage["lock"]:
        if frame_storage["latest_frame"] is None:
            return JsonResponse({"frame": None, "detections": []})

        import base64
        frame_base64 = base64.b64encode(frame_storage["latest_frame"]).decode("utf-8")
        return JsonResponse({"frame": frame_base64, "detections": frame_storage["detections"]})



@csrf_exempt
def stop_detection(request):
    if request.method == "POST":
        with frame_storage["lock"]:
            frame_storage["abort"] = True  # 设置终止标志

            home_app_config = apps.get_app_config('home')
            yolo_predict = home_app_config.yolo_predict
            yolo_predict.release_capture()

        return JsonResponse({"status": "detection stopped"})






@csrf_exempt
def set_model_view(request):
    if request.method == 'POST':
        try:
            if not request.body:
                return JsonResponse({"success": False, "error": "请求体为空"}, status=400)

            data = json.loads(request.body)
            model_name = data.get('model_name', '').strip()
            print(model_name)

            if not model_name:
                return JsonResponse({"success": False, "error": "未提供模型名称"}, status=400)


            model_path = os.path.join(settings.SAVEMODEL_ROOT, model_name)

            if not os.path.exists(model_path):
                return JsonResponse({"success": False, "error": f"模型文件 {model_name}.pt 不存在"}, status=400)

            home_app_config = apps.get_app_config('home')
            home_app_config.yolo_predict.new_model_name = model_path
            home_app_config.yolo_predict.load_yolo_model()

            return JsonResponse({"success": True, "message": f"模型 {model_name}.pt 加载成功"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON 解析失败"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "无效请求方法"}, status=405)






@csrf_exempt
def set_confidence_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            confidence = data.get('confidence')
            iou = data.get('iou')

            home_app_config = apps.get_app_config('home')
            home_app_config.yolo_predict.conf_thres = confidence
            home_app_config.yolo_predict.iou_thres = iou

            return JsonResponse({"success": True, "message": f"置信度设置为 {confidence}"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "JSON 解析失败"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "无效请求方法"}, status=405)


