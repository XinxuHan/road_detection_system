import json
import os
import threading
from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage, default_storage
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

from openai import OpenAI

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




import re

client = OpenAI(base_url="https://api.sambanova.ai/v1", api_key="c7ebcdfd-d744-4069-b4f0-485e96c86a58")


def parse_bbox(bbox):
    """
    将 "(x1, y1), (x2, y2)" 字符串解析为 dict。
    """
    try:
        matches = re.findall(r"\((\d+),\s*(\d+)\)", bbox)
        if len(matches) == 2:
            (x1, y1), (x2, y2) = matches
            return {
                "x1": int(x1),
                "y1": int(y1),
                "x2": int(x2),
                "y2": int(y2)
            }
    except Exception as e:
        print("⚠️ bbox 解析失败:", e)
    return {"x1": 0, "y1": 0, "x2": 0, "y2": 0}


@csrf_exempt
def analyze_llm_view(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "仅支持 POST 请求"}, status=405)

    try:
        data = json.loads(request.body)
        detections = data.get("results", [])
        task = data.get("task", "summary")

        if not detections:
            return JsonResponse({"success": False, "error": "Detection data is empty"})

        # 构造 prompt 内容
        # prompt_lines = []
        #
        # for result in detections:
        #     class_name = result.get("class_name", "未知")
        #     confidence = result.get("confidence", 0)
        #
        #     bbox_raw = result.get("bbox")
        #     if isinstance(bbox_raw, str):
        #         bbox = parse_bbox(bbox_raw)
        #     elif isinstance(bbox_raw, dict):
        #         bbox = bbox_raw
        #     else:
        #         bbox = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
        #
        #     prompt_lines.append(
        #         f"目标 {result.get('id', '?')} 是 {class_name}，置信度为 {confidence}%，"
        #         f"位于左上角({bbox['x1']}, {bbox['y1']}) 到右下角({bbox['x2']}, {bbox['y2']}) 的区域。"
        #     )
        #
        # prompt_context = "\n".join(prompt_lines)
        # prompt_task = {
        #     "summary": "请总结图像中的主要目标及其位置和置信度。",
        #     "risk_analysis": "请评估图像中的风险目标，判断是否存在安全隐患。",
        #     "road_guidance": "请基于检测结果给出合理的通行建议或路径引导。"
        # }.get(task, "请分析以下目标信息：")
        #
        # final_prompt = f"{prompt_task}\n\n检测结果如下：\n{prompt_context}"

        # 构造 Markdown 表格形式的 prompt（更适合 LLM 理解空间结构）
        table_lines = [
            "| ID | 类别 | 置信度 | 左上角坐标 | 右下角坐标 |",
            "|----|------|--------|----------------|----------------|"
        ]

        for result in detections:
            class_name = result.get("class_name", "未知")
            confidence = result.get("confidence", "0")
            bbox_raw = result.get("bbox")
            if isinstance(bbox_raw, str):
                bbox = parse_bbox(bbox_raw)
            elif isinstance(bbox_raw, dict):
                bbox = bbox_raw
            else:
                bbox = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}

            table_lines.append(
                f"| {result.get('id', '?')} | {class_name} | {confidence}% | "
                f"({bbox['x1']}, {bbox['y1']}) | ({bbox['x2']}, {bbox['y2']}) |"
            )

        prompt_context = "\n".join(table_lines)

        # 加强任务指令，引导 LLM 输出结构化结论
        prompt_task = {
            "summary": (
                "请根据以下检测结果，概括图像中存在的主要目标，指出它们的分布位置和数量，"
                "以及可能的场景类型（如停车场、道路拥堵、街道等）。"
            ),
            "risk_analysis": (
                "请从检测结果中分析是否存在潜在安全风险，例如视野遮挡、异常靠近边缘、密集分布等，"
                "并根据目标位置和类别评估风险等级与原因。"
            ),
            "road_guidance": (
                "请结合目标的位置、类别和分布情况，为当前场景提供合理的通行建议或避让策略。"
                "指出可通行区域、建议避让的高密度或危险区域，并说明依据。"
            )
        }.get(task, "请分析以下检测结果，给出你的专业判断。")

        final_prompt = (
            "你是一位道路图像分析专家，擅长结合目标检测结果评估交通状况、安全风险以及通行建议。\n\n"
            f"{prompt_task}\n\n"
            f"以下是检测到的目标信息（结构化表示）：\n{prompt_context}"
        )


        # 调用 LLM API（非流式）
        completion = client.chat.completions.create(
            model="Meta-Llama-3.1-405B-Instruct",
            messages=[
                {"role": "system", "content": ("你是一位经验丰富的交通图像分析专家, 擅长根据车辆等目标的类别, 置信度和空间位置." 
                                               "判断道路风险, 交通密度和合理通行路径. 请依据结构化输入信息, 给出逻辑严谨, 表达清晰, 结论明确的分析建议.")},
                {"role": "user", "content": final_prompt}
            ],
            stream=False
        )

        result_text = completion.choices[0].message.content
        return JsonResponse({
            "success": True,
            "analysis": result_text
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
