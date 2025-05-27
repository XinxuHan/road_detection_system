<template>
  <div id="mr-mainbody" class="container mr-mainbody">
    <!-- 第一行 -->
    <div class="control-panel">
      <el-select v-model="value" placeholder="默认模型" style="width: 800px" size="large" @change="handleModelChange">
        <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value" />
      </el-select>

      <el-button type="primary" style="width: 130px; height: 40px;" @click="triggerFileInput">
        选择图像
      </el-button>

      <el-button
          type="primary"
          style="width:130px; height: 40px;"
          @click="triggerVideoInput">
        选择视频
      </el-button>

      <el-button
          type="primary"
          style="width:130px; height: 40px;"
          @click="showCameraDialog"
      >
        摄像头检测
      </el-button>

      <!-- 摄像头选择对话框 -->
      <el-dialog
          v-model="cameraDialogVisible"
          title="选择摄像头"
          width="30%"
          @closed="resetCameraSelection"
      >
        <el-select
            v-model="selectedCamera"
            placeholder="请选择摄像头设备"
            @change="onCameraChange"
        >
          <el-option
              v-for="(camera, index) in cameraList"
              :key="index"
              :label="`摄像头 ${index} (${camera.label})`"
              :value="index"
          />

        </el-select>
      </el-dialog>






      <span class="confidence-label">置信度：</span>
      <el-slider style="width: 50%" v-model="conf_value" :format-tooltip="formatTooltip" @change="() => updateModelParams('confidence')" />
      <span>IoU：</span>
      <el-slider style="width: 50%" v-model="iou_value" :format-tooltip="formatTooltip" @change="() => updateModelParams('iou')" />

      <!--      <el-button class="fixed-btn" :type="loading ? 'info' : 'primary'" :loading="loading" @click="uploadAndStyleTransfer" :disabled="loading" style="width: 130px; height: 40px;">-->
      <!--        {{ loading ? '正在上传...' : '开始检测' }}-->
      <!--      </el-button>-->

      <el-button
          class="fixed-btn"
          :type="loading ? 'info' : 'primary'"
          :loading="loading"
          @click="uploadAndStyleTransfer"
          :disabled="loading"
          style="width: 130px; height: 40px;">
        {{ loading ? '正在检测...' : '开始检测' }}
      </el-button>


      <el-button type="primary" style="width: 130px; height: 40px;" @click="stopDetection">
        结束视频检测
      </el-button>

    </div>

    <!-- 第二行：图片显示区域 -->
    <div class="image-container">
      <div class="imagePreview">
        <video
            v-if="currentMediaType === 'video' && mediaUrl"
            :src="mediaUrl"
            controls
            class="preview-media">
        </video>

        <img
            v-else-if="currentMediaType === 'image' && mediaUrl"
            :src="mediaUrl"
            alt="Content Media"
            class="preview-media">

        <input
            type="file"
            id="imageInput"
            style="display: none;"
            @change="handleImageUpload"
            accept="image/*">

        <input
            type="file"
            id="videoInput"
            style="display: none;"
            @change="handleVideoUpload"
            accept="video/*">


      </div>



      <div class="imagePreview">
        <img v-if="resultImageUrl" :src="resultImageUrl" class="preview-media"  >
      </div>
    </div>

    <!-- 表格区域 -->
    <div class="content-table">
      <el-table :data="tableData" style="width: 100%" :row-class-name="tableRowClassName">
        <el-table-column prop="id" label="类别ID" width="180" />
        <el-table-column prop="class_name" label="类别" width="180" />
        <el-table-column prop="conf" label="置信度" width="180" />
        <el-table-column prop="bbox" label="目标坐标" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue';
import {ElMessage} from "element-plus";
import axios from "axios";
import {setModelParams, switchModel} from "@/api/yolo/model";
const resultImageUrl = ref<string | null>(null);
const loading = ref(false);

// const currentMediaType = ref<'image' | 'video'>('image');
const currentMediaType = ref<'image' | 'video' | 'camera'>('image');
const mediaUrl = ref<string | null>(null);


const videoFile = ref<File | null>(null);
let pollingInterval: number | null = null;



// 摄像头
const cameraDialogVisible = ref(false);
const cameraList = ref<MediaDeviceInfo[]>([]);
const selectedCamera = ref('')
const resetCameraSelection = () => {
  selectedCamera.value = '';
};


// 获取摄像头列表
const showCameraDialog = async () => {
  try {
    // 先请求摄像头权限
    await navigator.mediaDevices.getUserMedia({ video: true });

    const devices = await navigator.mediaDevices.enumerateDevices();
    cameraList.value = devices.filter(d => d.kind === 'videoinput');

    if (cameraList.value.length === 0) {
      ElMessage.warning("未找到可用摄像头");
      return;
    }

    cameraDialogVisible.value = true;
  } catch (error) {
    ElMessage.error("摄像头访问被拒绝或不可用");
    console.error("摄像头访问错误:", error);
  }
};



const onCameraChange = async (deviceIndex: number) => {
  await startCameraDetection(deviceIndex);
  cameraDialogVisible.value = false; // 关闭对话框
};




const startCameraDetection = async (deviceIndex: number) => {
  await stopDetection(); // 先停止上一次检测
  loading.value = true;
  try {
    const response = await fetch("http://localhost:8000/api/start-camera", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        camera_index: deviceIndex,
        iou: iou_value.value / 100,
        conf: conf_value.value / 100
      }),
    });

    if (response.ok) {
      currentMediaType.value = "camera";
      pollResultsCamera(); // 轮询摄像头检测结果
      ElMessage.success("摄像头检测已启动");
    }
  } catch (err) {
    console.error("启动摄像头检测失败:", err);
    loading.value = false;
  }
};



const value = ref('')

const options = [
  {
    value: 'yolo11n.pt',
    label: 'yolo11n.pt',
  },
  {
    value: 'yolo11n-pose.pt',
    label: 'yolo11n-pose.pt',
  },
  {
    value: 'yolo11n-seg.pt',
    label: 'yolo11n-seg.pt',
  },
]

const handleModelChange = async () => {
  if (!value.value) {
    ElMessage.warning("请选择一个模型");
    return;
  }

  try {
    const response = await switchModel(value.value);
    console.log("服务器响应:", response.data);
    if (response.data.success) {
      ElMessage.success(`模型切换成功: ${value.value}`);
    } else {
      ElMessage.error(`切换失败: ${response.data.error}`);
    }
  } catch (error) {
    console.error("网络请求错误:", error);
    ElMessage.error("网络请求失败");
  }
};




const iou_value = ref(70)
const conf_value = ref(45)


const formatTooltip = (val: number) => {
  return val / 100
}

const updateModelParams = async (changedParam: "confidence" | "iou") => {
  try {
    const response = await setModelParams(conf_value.value / 100, iou_value.value / 100);
    console.log("服务器响应:", response.data);

    if (response.data.success) {
      if (changedParam === "confidence") {
        ElMessage.success(`置信度更新成功: ${conf_value.value/ 100}`);
      } else if (changedParam === "iou") {
        ElMessage.success(`IoU 更新成功: ${iou_value.value/ 100}`);
      }
    } else {
      ElMessage.error(`更新失败: ${response.data.error}`);
    }
  } catch (error) {
    console.error("网络请求错误:", error);
    ElMessage.error("参数更新失败");
  }
};



interface DetectionResult {
  id: number;
  class_name: string;  // 类别名称
  conf: string;        // 置信度
  bbox: {              // 坐标
    x1: number;
    y1: number;
    x2: number;
    y2: number;
  };
}

const tableRowClassName = ({ rowIndex }: { rowIndex: number }) => {
  if (rowIndex % 4 === 1) return "primary-row";
  if (rowIndex % 4 === 3) return "success-row";
  return "";
};


const tableData = ref<DetectionResult[]>([]);



// 选择图片
const triggerFileInput = () => {
  const fileInput = document.getElementById('imageInput') as HTMLInputElement;
  if (fileInput) {
    fileInput.click();  // 点击事件
  }
};

const triggerVideoInput = () => {
  const fileInput = document.getElementById('videoInput') as HTMLInputElement;
  fileInput?.click();
};


// 预览图片功能
const handleImageUpload = (event: Event) => {
  currentMediaType.value = 'image';
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = () => {
      mediaUrl.value = reader.result as string; // 设置图片预览 URL
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    mediaUrl.value = null; // 清除预览
  }
};



// 处理文件上传
const handleVideoUpload = (event: Event) => {
  currentMediaType.value = 'video';
  const input = event.target as HTMLInputElement;
  if (!input.files?.[0]) return;

  videoFile.value = input.files[0];
  mediaUrl.value = URL.createObjectURL(videoFile.value);

};



const uploadAndStyleTransfer = async () => {
  loading.value = true;  // 设置加载状态

  if (currentMediaType.value === "image") {
    // 处理图片检测
    const formData = new FormData();
    const input = document.getElementById("imageInput") as HTMLInputElement;
    if (input.files && input.files[0]) {
      formData.append("content_image", input.files[0]);
    }

    try {
      const response = await fetch("http://localhost:8000/detect/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      loading.value = false;

      if (data.image_url) {
        resultImageUrl.value = `http://localhost:8000${data.image_url}`;
      }

      if (data.results) {
        tableData.value = data.results.map((item: any) => ({
          id: item.id,
          class_name: item.class_name,
          conf: item.confidence + "%",
          bbox: `(${item.bbox.x1}, ${item.bbox.y1}), (${item.bbox.x2}, ${item.bbox.y2})`,
        }));
      } else {
        console.error("响应中缺少处理后图像的URL.");
      }
    } catch (error) {
      loading.value = false;
      console.error("Error:", error);
    }
  } else if (currentMediaType.value === "video") {
    // 处理视频检测
    if (!videoFile.value) {
      ElMessage.warning("请先选择一个视频！");
      loading.value = false;
      return;
    }

    const formData = new FormData();
    formData.append("video", videoFile.value);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload-video/", {
        method: "POST",
        body: formData,
      });


      if (response.ok) {
        console.log("视频上传成功，开始轮询检测帧...");
        pollResults();
      } else {
        console.error("视频上传失败");
      }
    } catch (error) {
      console.error("视频上传失败:", error);
    }
  }
};


let lastFrameId = ref(0);
// 轮询获取视频帧
const pollResults = async () => {
  pollingInterval = window.setInterval(async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/get-frame/")
      const data = await response.json()

      if (data.frame_id && data.frame_id !== lastFrameId.value) {
        resultImageUrl.value = data.frame_url
        lastFrameId.value = data.frame_id
      }else {
        resultImageUrl.value = null; // **清空显示**
      }

      // 更新表格数据
      if (data.detections) {
        tableData.value = data.detections.map((item: any) => ({
          id: item.id,
          class_name: item.class_name,
          conf: item.confidence + "%" ,
          bbox: `(${item.bbox.x1}, ${item.bbox.y1}), (${item.bbox.x2}, ${item.bbox.y2})`
        }));
      }
      if (!data.processing) {
        if (pollingInterval) {
          clearInterval(pollingInterval)
          pollingInterval = null
        }
        loading.value = false
      }
    } catch (error) {
      console.error("轮询失败:", error)
      if (pollingInterval) clearInterval(pollingInterval)
      loading.value = false
    }
  }, 300) // 轮询间隔300ms
}



const pollResultsCamera = () => {
  if (pollingInterval) clearInterval(pollingInterval);

  pollingInterval = setInterval(async () => {
    try {
      const response = await fetch("http://localhost:8000/api/get-latest-frame");
      if (!response.ok) throw new Error("请求失败");

      const data = await response.json();
      if (data.frame) {
        resultImageUrl.value = `data:image/jpeg;base64,${data.frame}`; // 更新图片
      }else {
        resultImageUrl.value = null; // 清空
      }
      // 更新表格数据
      if (data.detections) {
        tableData.value = data.detections.map((item: any) => ({
          id: item.id,
          class_name: item.class_name,
          conf: item.confidence + "%" ,
          bbox: `(${item.bbox.x1}, ${item.bbox.y1}), (${item.bbox.x2}, ${item.bbox.y2})`
        }));
      }
    } catch (error) {
      console.error("轮询失败:", error);
      resultImageUrl.value = null;
    }
  }, 500); // 500ms 请求一次
};




const stopDetection = async () => {
  try {
    await fetch("http://127.0.0.1:8000/api/stop_detection/", {
      method: "POST"
    });

    // 强制重置前端状态
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
    loading.value = false;
    resultImageUrl.value = null;

  } catch (error) {
    console.error("终止请求失败:", error);

  }
};




</script>




<style scoped>


.control-panel {
  position: relative;
  width: 1200px !important;
  left: -2%;
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: space-between;

}



.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  margin-top: 35px;
}

.imagePreview {
  height: 370px;
  width: 550px;
  border: 1px solid #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
}

.content-table {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin: auto;
  margin-top: 40px;
  margin-bottom: 10vh;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.confidence-label {
  flex-shrink: 0;
  min-width: 70px;
  text-align: right;
  font-size: 14px;
  color: #606266;
}


.preview-media {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
}



</style>




<style>
.el-table .primary-row {
  --el-table-tr-bg-color: var(--el-color-primary-light-9);
}

.el-table .success-row {
  --el-table-tr-bg-color: var(--el-color-success-light-9);
}
</style>