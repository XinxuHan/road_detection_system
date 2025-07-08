import json
import os
import threading
import re
import time

from django.apps import apps
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from home.detectors.image_detect import detect
from home.detectors.video_detect import process_video
from home.detectors.camera_detect import process_camera
from home.frame_state import frame_storage

from openai import OpenAI




@csrf_exempt
def recognition_view(request):
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
def upload_video_view(request):
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
def start_camera_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            camera_index = int(data.get("camera_index", 0))

            # 停止正在进行的检测
            with frame_storage["lock"]:
                if frame_storage["processing"]:
                    frame_storage["stop"] = True

            # 启动摄像头检测线程
            thread = threading.Thread(target=process_camera, args=(camera_index,))
            thread .start()

            return JsonResponse({
                "message": f"摄像头{camera_index}检测已启动",
                "camera_index": camera_index
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)






def get_frame_view(request):
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




def get_latest_frame_view(request):
    with frame_storage["lock"]:
        if frame_storage["latest_frame"] is None:
            return JsonResponse({"frame": None, "detections": []})

        import base64
        frame_base64 = base64.b64encode(frame_storage["latest_frame"]).decode("utf-8")
        return JsonResponse({"frame": frame_base64, "detections": frame_storage["detections"]})



@csrf_exempt
def stop_recognition_view(request):
    if request.method == "POST":
        with frame_storage["lock"]:
            frame_storage["stop"] = True  # 设置终止标志

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




client = OpenAI(base_url="https://api.sambanova.ai/v1", api_key="c7ebcdfd-d744-4069-b4f0-485e96c86a58")


def parse_bbox(bbox):
    """
    Parse the strings "(x1, y1), (x2, y2)" into dict.
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
        print("bbox Parsing failed: ", e)
    return {"x1": 0, "y1": 0, "x2": 0, "y2": 0}



@csrf_exempt
def analyze_llm_view(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST requests are supported"}, status=405)

    try:
        data = json.loads(request.body)
        detections = data.get("results", [])
        task = data.get("task", "zero_shot")
        selected_model = data.get("llm_model", "Llama-4-Maverick-17B-128E-Instruct")  # Support model switching

        # Safe filtering allows only preset models
        available_models = [
            "Meta-Llama-3.1-405B-Instruct",
            "Meta-Llama-3.1-8B-Instruct",
            "Llama-4-Maverick-17B-128E-Instruct",
            "Qwen3-32B",
            "DeepSeek-R1-0528"
            # More can be added
        ]
        if selected_model not in available_models:
            return JsonResponse({
                "success": False,
                "error": f"Unsupported model types: {selected_model}"
            }, status=400)

        if not detections:
            return JsonResponse({"success": False, "error": "Detection data is empty"})

        table_lines = [
            "| ID | Class | Confidence | Coordinate of the upper left corner | Coordinates at the lower right corner |",
            "|----|------|--------|----------------|----------------|"
        ]
        for result in detections:
            class_name = result.get("class_name", "Unknown")
            confidence = result.get("confidence", "0")
            bbox_raw = result.get("bbox")
            bbox = parse_bbox(bbox_raw) if isinstance(bbox_raw, str) else bbox_raw or {}

            table_lines.append(
                f"| {result.get('id', '?')} | {class_name} | {confidence}% | "
                f"({bbox.get('x1', 0)}, {bbox.get('y1', 0)}) | ({bbox.get('x2', 0)}, {bbox.get('y2', 0)}) |"
            )
        prompt_context = "\n".join(table_lines)

        print(prompt_context)

        # Prompt word construction
        prompt_task = {
            "zero_shot": (
                "As an expert in autonomous driving image analysis, please determine whether the current vehicle can "
                "pass safely based on the structured detection form provided below and offer operational suggestions.\n"
                "Each row in the table represents a detected target, and the field descriptions are as follows:\n"
                "- Class: The semantic category of the target (e.g. car, person, traffic light, etc., from the IDD "
                "dataset)\n"
                "- Confidence: The probability (percentage) of recognition accuracy\n"
                "- Coordinates: Indicate the spatial position of the target in the image (upper left corner and lower "
                "right corner)\n\n"
                "Please complete the following tasks strictly based on the table data:\n"
                "1. Determine whether it is currently passable and whether there are any traffic obstructions or "
                "potential risks.\n"
                "2. Give clear driving advice (such as: slow down, stop and wait, give way, drive in the center, "
                "etc.);\n"
                "It is prohibited to fabricate categories or scenarios not listed in the table. The language should "
                "be concise and professional.\n"
                "You should give the Operational Suggestion directly."
            ),

            "cot": (
                "Question: \n"
                "As an expert in autonomous driving image analysis, please determine whether the current vehicle can "
                "pass safely based on the structured detection form provided below and offer operational "
                "suggestions.\n\n"
                "| ID | Class | Confidence | Coordinate of the upper left corner | Coordinates at the lower right "
                "corner |\n"
                "|----|------|--------|----------------|----------------|\n"
                "| 1 | out of roi | 95% | (1501, 237) | (1920, 716) |\n"
                "| 2 | border | 90% | (919, 524) | (1897, 1080) |\n"
                "| 3 | road | 81% | (21, 496) | (1858, 1080) |\n"
                "| 4 | sky | 77% | (0, 0) | (1859, 511) |\n"
                "| 5 | vegetation | 72% | (50, 111) | (575, 563) |\n"
                "| 6 | vegetation | 69% | (623, 340) | (733, 488) |\n"
                "| 7 | border | 62% | (7, 537) | (723, 833) |\n"
                "| 8 | vegetation | 56% | (757, 419) | (848, 495) |\n"
                "| 9 | vegetation | 47% | (1130, 315) | (1591, 636) |\n"
                "| 10 | fence | 47% | (855, 477) | (930, 555) |\n"
                "| 11 | vegetation | 38% | (853, 436) | (908, 482) |\n"
                "| 12 | vegetation | 35% | (942, 420) | (1042, 534) |\n"
                "| 13 | vegetation | 32% | (1068, 375) | (1201, 495) |\n"
                "| 14 | vegetation | 32% | (1066, 421) | (1263, 605) |\n"
                "| 15 | vegetation | 31% | (722, 422) | (812, 494) |\n"
                "| 16 | vegetation | 26% | (657, 404) | (755, 501) |\n\n"
                "Answer: \n"
                "【Step 1】\n"
                "- `road` (81%) with coordinates (21, 496) to (1858, 1080), covering almost the entire lower half of "
                "the image horizontally;\n"
                "- Multiple `vegetation` objects (16 instances, confidence between 26% to 72%) appearing along the "
                "left and right borders, especially concentrated from (50, 111) to (1263, 605);\n"
                "- `border` (90%, 62%) detected on both left and right sides, likely indicating curbside or shoulder "
                "edges;\n"
                "- One `fence` (47%) on the right side around (855, 477) to (930, 555), suggesting physical "
                "containment;\n"
                "- `out of roi` (95%) object located in the far right upper region, possibly outside the usable image "
                "space.\n\n"
                "【Step 2】\n"
                "Risk assessment:\n"
                "- The road area appears clear and continuous, without major obstructions within the drivable region;\n"
                "- Vegetation intrusions are visible on both sides of the road, especially dense on the right side, "
                "which may slightly reduce usable lane width;\n"
                "- No traffic lights, vehicles, or pedestrians are detected—this may limit situational awareness but "
                "does not inherently suggest danger;\n"
                "- Right border and fence indicate a constrained edge, and combined with vegetation may cause "
                "right-side crowding;\n"
                "- Sky occupies the upper half of the image, which is normal and not a risk factor.\n\n"
                "【Step 3】\n"
                "The current scene is generally safe for driving. The road is well-detected, unobstructed, "
                "and wide enough for single-lane forward movement. While right-side vegetation and fence limit "
                "lateral flexibility, the central lane appears navigable. However, the absence of dynamic agents ("
                "vehicles, people) suggests this may be a rural or quiet road, requiring cautious forward "
                "monitoring.\n\n"
                "【Step 4】\n"
                "Driving recommendation:\n"
                "1. Maintain current lane position and drive centered within the detected road area.\n"
                "2. Avoid drifting toward the right edge due to vegetation and fence boundary.\n"
                "3. Proceed with moderate speed and visual caution, as undetected dynamic elements (e.g., vehicles, "
                "humans) may appear beyond current perception range.\n"

                "Question: \n"

            ),

            "few_shot": (
                "The following is an example of generating driving suggestions based on target recognition results. "
                "Please refer to the example style and analyze based on the new table input:\n\n"
                "Example 1: \n"
                "| ID | Class | Confidence | Coordinate of the upper left corner | Coordinates at the lower right |\n"
                "|----|------|--------|----------------|----------------|\n"
                "| 1 | car | 93% | (100, 200) | (400, 600) |\n"
                "| 2 | traffic light | 90% | (300, 100) | (320, 150) |\n"
                "Analysis: A vehicle ahead and a red light signal have been detected. It is recommended to "
                "immediately slow down and stop, and wait for the signal to change.\n\n"
                "Example 2: \n"
                "| ID | Class | Confidence | Coordinate of the upper left corner | Coordinates at the lower right |\n"
                "|----|------|--------|----------------|----------------|\n"
                "| 1 | person | 85% | (500, 300) | (550, 500) |\n"
                "| 2 | bus | 92% | (150, 220) | (350, 500) |\n"
                "Analysis: There are buses and pedestrians ahead. It is recommended to drive on the right and slow "
                "down to avoid them to ensure safety.\n\n"
                "Please complete according to the data in the detection form below:\n"
                "1. Whether the current road is passable;\n"
                "2. Existing risks and obstacles;\n"
                "3. Specific driving suggestions. The language should be clear and professional, following the above "
                "style. Do not fabricate content that does not appear in the table."
            )
        }.get(task, "Please analyze the following results and provide your professional judgment.")

        final_prompt = (
            "As an expert in autonomous driving image analysis, please determine whether the current vehicle can pass "
            "safely based on the structured detection form provided below and offer operational suggestions.\n\n"
            f"{prompt_task}\n\n"
            f"The following is the detected object information (structured representation) :\n{prompt_context}"
        )

        start_time = time.time()
        completion = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": (
                    "You are an experienced expert in autonomous driving image analysis, skilled at analyzing based "
                    "on the category, confidence level and spatial position of targets such as vehicles,"
                    "Judge road risks, traffic density and reasonable passage routes. Please provide suggestions that "
                    "are logically rigorous, clearly expressed and have definite conclusions based on the structured "
                    "input information."
                    )},
                {"role": "user", "content": final_prompt}
            ],
            stream=False
        )

        result_text = completion.choices[0].message.content

        usage = getattr(completion, "usage", None)
        total_tokens = usage.total_tokens if usage else None
        inference_time = round(time.time() - start_time, 3)

        result_text += f"\n\n⏱️ Reasoning time: {inference_time} seconds"
        if total_tokens:
            result_text += f"\n📊 Total tokens used: {total_tokens}"

        return JsonResponse({
            "success": True,
            "analysis": result_text
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)