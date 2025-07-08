<template>
  <div id="mr-mainbody" class="container mr-mainbody">

    <!-- 按钮与参数调节区域 -->
    <div class="control-panel">
      <!-- 第一行按钮 -->
      <div class="control-row">
        <el-select v-model="value" placeholder="Default Model" style="width: 300px" size="large" @change="handleModelChange">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>

        <el-button type="primary" @click="triggerFileInput">Select Image</el-button>
        <el-button type="primary" @click="triggerVideoInput">Select Video</el-button>
        <el-button type="primary" @click="showCameraDialog">Camera Detection</el-button>
      </div>

      <!-- 第二行参数和控制按钮 -->
      <div class="control-row">
        <span class="confidence-label">Confidence:</span>
        <el-slider style="width: 160px" v-model="conf_value" :format-tooltip="formatTooltip" @change="() => updateModelParams('confidence')" />

        <span class="confidence-label">IoU:</span>
        <el-slider style="width: 160px" v-model="iou_value" :format-tooltip="formatTooltip" @change="() => updateModelParams('iou')" />

        <el-button :type="loading ? 'info' : 'primary'" :loading="loading" @click="uploadAndStyleTransfer" :disabled="loading">
          {{ loading ? 'Detecting...' : 'Start Detecting' }}
        </el-button>

        <el-button type="primary" @click="stopDetection">End Detection</el-button>
        <el-button type="success" :disabled="!resultImageUrl" @click="downloadImage">Save Image</el-button>
        <el-button type="success" :disabled="tableData.length === 0" @click="downloadCSV">Save CSV</el-button>
      </div>
    </div>

    <!-- 媒体预览区域 -->
    <div class="image-container">
      <div class="imagePreview">
        <video v-if="currentMediaType === 'video' && mediaUrl" :src="mediaUrl" controls class="preview-media" />
        <img v-else-if="currentMediaType === 'image' && mediaUrl" :src="mediaUrl" alt="Content Media" class="preview-media" />
        <input type="file" id="imageInput" style="display: none;" @change="handleImageUpload" accept="image/*" />
        <input type="file" id="videoInput" style="display: none;" @change="handleVideoUpload" accept="video/*" />
      </div>

      <div class="imagePreview">
        <img v-if="resultImageUrl" :src="resultImageUrl" class="preview-media" />
      </div>
    </div>

    <!-- 检测结果表格 -->
    <div class="content-table">
      <el-table :data="tableData" style="width: 100%" :row-class-name="tableRowClassName">
        <el-table-column prop="id" label="ID" width="180" />
        <el-table-column prop="class_name" label="Class" width="180" />
        <el-table-column prop="conf" label="Confidence" width="180" />
        <el-table-column prop="bbox" label="BBox" />
      </el-table>

      <!-- LLM 分析结果 -->
      <div class="llm-analysis-section" style="margin-top: 30px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
          <span style="font-weight: bold; font-size: 15px;">🔍 Select the prompt engineering method:</span>
          <el-select v-model="selectedLlmTask" placeholder="Select the prompt method" style="width: 300px;">
            <el-option v-for="item in llmTaskOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>

        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
          <span style="font-weight: bold; font-size: 15px;">🤖 Select the large language model:</span>
          <el-select v-model="selectedLlmModel" placeholder="Select the large language model" style="width: 300px;">
            <el-option v-for="item in llmModelOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>


        <div style="border: 1px solid #ccc; border-radius: 6px; padding: 8px;">
          <el-input
              type="textarea"
              v-model="llmResult"
              placeholder="The LLM analysis results will be displayed here"
              autosize
              readonly
              style="width: 100%; font-family: monospace;"
          />
        </div>

      </div>
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



// Camera
const cameraDialogVisible = ref(false);
const cameraList = ref<MediaDeviceInfo[]>([]);
const selectedCamera = ref('')
const resetCameraSelection = () => {
  selectedCamera.value = '';
};


// Get the camera list
const showCameraDialog = async () => {
  try {
    // Request camera permission first
    await navigator.mediaDevices.getUserMedia({ video: true });

    const devices = await navigator.mediaDevices.enumerateDevices();
    cameraList.value = devices.filter(d => d.kind === 'videoinput');

    if (cameraList.value.length === 0) {
      ElMessage.warning("No available cameras found");
      return;
    }

    cameraDialogVisible.value = true;
  } catch (error) {
    ElMessage.error("Camera access denied or unavailable");
    console.error("Camera access error:", error);
  }
};



const onCameraChange = async (deviceIndex: number) => {
  await startCameraDetection(deviceIndex);
  cameraDialogVisible.value = false; // Close dialog box
};




const startCameraDetection = async (deviceIndex: number) => {
  await stopDetection(); // Stop the last test first
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
      pollResultsCamera(); // Polling camera detection results
      ElMessage.success("Camera detection started");
    }
  } catch (err) {
    console.error("Failed to start camera detection:", err);
    loading.value = false;
  }
};


// LLM 分析相关
const selectedLlmTask = ref("zero_shot");
const llmResult = ref("");

const llmTaskOptions = [
  { value: "zero_shot", label: "Zero-Shot Prompting" },
  { value: "cot", label: "Chain-of-Thought (CoT) Prompting" },
  { value: "few_shot", label: "Few-Shot Prompting" },
];

// 调用后端分析接口
const analyzeWithLLM = async () => {
  if (tableData.value.length === 0) {
    llmResult.value = "⚠️ 当前无检测目标，无法分析。";
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/api/analyze-llm/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        results: tableData.value.map(item => ({
          id: item.id,
          class_name: item.class_name,
          confidence: parseFloat(item.conf.replace("%", "")),
          bbox: item.bbox,
        })),
        task: selectedLlmTask.value,
        llm_model: selectedLlmModel.value,
      }),
    });

    const result = await response.json();
    if (result.success) {
      llmResult.value = result.analysis;
    } else {
      llmResult.value = "❌ 分析失败：" + result.error;
    }
  } catch (e) {
    llmResult.value = "❌ 分析请求失败：" + e;
    console.error("LLM分析异常:", e);
  }
};


const selectedLlmModel = ref("Llama-4-Maverick-17B-128E-Instruct");

const llmModelOptions = [
  { value: "Meta-Llama-3.1-405B-Instruct", label: "Meta-Llama-3.1-405B-Instruct" },
  { value: "Meta-Llama-3.1-8B-Instruct", label: "Meta-Llama-3.1-8B-Instruct" },
  { value: "Llama-4-Maverick-17B-128E-Instruct", label: "Llama-4-Maverick-17B-128E-Instruct" },
  { value: "Qwen3-32B", label: "Qwen3-32B" },
  { value: "DeepSeek-R1-0528", label: "DeepSeek-R1-0528" }
];




const value = ref('')

const options = [
  {
    value: 'yolo8-best.pt',
    label: 'yolo8-best.pt',
  },
  {
    value: 'yolo11-best.pt',
    label: 'yolo11-best.pt',
  },
  {
    value: 'yolo11.pt',
    label: 'yolo11.pt',
  },
  {
    value: 'yolo11n-seg.pt',
    label: 'yolo11n-seg.pt',
  },
  {
    value: 'best.pt',
    label: 'best.pt',
  },
  {
    value: 'last.pt',
    label: 'last.pt',
  },
]

const handleModelChange = async () => {
  if (!value.value) {
    ElMessage.warning("Please select a model");
    return;
  }

  try {
    const response = await switchModel(value.value);
    console.log("Server Response:", response.data);
    if (response.data.success) {
      ElMessage.success(`Model switching successful: ${value.value}`);
    } else {
      ElMessage.error(`Switch failed: ${response.data.error}`);
    }
  } catch (error) {
    console.error("Network request error:", error);
    ElMessage.error("Network request failed");
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
    console.log("Server Response:", response.data);

    if (response.data.success) {
      if (changedParam === "confidence") {
        ElMessage.success(`Confidence updated successfully: ${conf_value.value/ 100}`);
      } else if (changedParam === "iou") {
        ElMessage.success(`IoU updated successfully: ${iou_value.value/ 100}`);
      }
    } else {
      ElMessage.error(`Update failed:${response.data.error}`);
    }
  } catch (error) {
    console.error("Network request error:", error);
    ElMessage.error("Parameter update failed");
  }
};



interface DetectionResult {
  id: number;
  class_name: string;  // Category Name
  conf: string;        // Confidence
  bbox: {              // coordinate
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



// Select image
const triggerFileInput = () => {
  const fileInput = document.getElementById('imageInput') as HTMLInputElement;
  if (fileInput) {
    fileInput.click();  // Click Event
  }
};

const triggerVideoInput = () => {
  const fileInput = document.getElementById('videoInput') as HTMLInputElement;
  fileInput?.click();
};


// Preview image function
const handleImageUpload = (event: Event) => {
  currentMediaType.value = 'image';
  const input = event.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = () => {
      mediaUrl.value = reader.result as string; // Set the image preview URL
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    mediaUrl.value = null; // Clear Preview
  }
};



// Handling file uploads
const handleVideoUpload = (event: Event) => {
  currentMediaType.value = 'video';
  const input = event.target as HTMLInputElement;
  if (!input.files?.[0]) return;

  videoFile.value = input.files[0];
  mediaUrl.value = URL.createObjectURL(videoFile.value);

};



const uploadAndStyleTransfer = async () => {
  loading.value = true;  // Set loading state

  if (currentMediaType.value === "image") {
    // Processing image detection
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

        // 自动调用 LLM 分析
        await analyzeWithLLM();

      } else {
        console.error("The URL to the processed image is missing from the response.");
      }
    } catch (error) {
      loading.value = false;
      console.error("Error:", error);
    }
  } else if (currentMediaType.value === "video") {
    // Processing video detection
    if (!videoFile.value) {
      ElMessage.warning("Please select a video first!");
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
        console.log("The video was uploaded successfully, and the polling detection frame started...");
        pollResults();
      } else {
        console.error("Video upload failed");
      }
    } catch (error) {
      console.error("Video upload failed:", error);
    }
  }
};


let lastFrameId = ref(0);
// Polling to get video frames
const pollResults = async () => {
  pollingInterval = window.setInterval(async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/get-frame/")
      const data = await response.json()

      if (data.frame_id && data.frame_id !== lastFrameId.value) {
        resultImageUrl.value = data.frame_url
        lastFrameId.value = data.frame_id
      }else {
        resultImageUrl.value = null; // **Clear display**
      }

      // Update table data
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
      console.error("Polling failed:", error)
      if (pollingInterval) clearInterval(pollingInterval)
      loading.value = false
    }
  }, 300) // Polling interval 300ms
}



const pollResultsCamera = () => {
  if (pollingInterval) clearInterval(pollingInterval);

  pollingInterval = setInterval(async () => {
    try {
      const response = await fetch("http://localhost:8000/api/get-latest-frame");
      if (!response.ok) throw new Error("Request failed");

      const data = await response.json();
      if (data.frame) {
        resultImageUrl.value = `data:image/jpeg;base64,${data.frame}`; // Update image
      }else {
        resultImageUrl.value = null; // clear
      }
      // Update table data
      if (data.detections) {
        tableData.value = data.detections.map((item: any) => ({
          id: item.id,
          class_name: item.class_name,
          conf: item.confidence + "%" ,
          bbox: `(${item.bbox.x1}, ${item.bbox.y1}), (${item.bbox.x2}, ${item.bbox.y2})`
        }));
      }
    } catch (error) {
      console.error("Polling failed:", error);
      resultImageUrl.value = null;
    }
  }, 500); // 500ms request once
};




const stopDetection = async () => {
  try {
    await fetch("http://127.0.0.1:8000/api/stop_detection/", {
      method: "POST"
    });

    // Force reset of frontend state
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
    loading.value = false;
    resultImageUrl.value = null;

  } catch (error) {
    console.error("Termination request failed:", error);

  }
};


const downloadImage = async () => {
  if (!resultImageUrl.value) {
    return ElMessage.warning('还没有检测结果');
  }

  try {
    // Pull image resources
    const res = await fetch(resultImageUrl.value);
    if (!res.ok) throw new Error(`网络错误：${res.status}`);
    // Convert to binary Blob
    const blob = await res.blob();
    // Generating a temporary object URL
    const url = URL.createObjectURL(blob);

    // Create an <a> and trigger a download
    const a = document.createElement('a');
    a.href = url;
    // Extract file name
    const segments = resultImageUrl.value.split('/');
    a.download = segments[segments.length - 1];
    document.body.appendChild(a);
    a.click();
    a.remove();

    // Release URL
    URL.revokeObjectURL(url);

    ElMessage.success('Download started');
  } catch (err) {
    console.error(err);
    ElMessage.error('Download failed, please try again');
  }
};


const downloadCSV = () => {
  if (tableData.value.length === 0) {
    return ElMessage.warning("There are currently no test results");
  }

  // Header
  const headers = ["ID", "Class", "Confidence", "BBox"];
  // Data for each row
  const rows = tableData.value.map(item => [
    item.id,
    item.class_name,
    item.conf,
    item.bbox,
  ]);

  // Scrape CSV text
  let csv = headers.join(",") + "\n"
          + rows.map(r => r.map(cell => `"${cell}"`).join(",")).join("\n");

  // Construction Download
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  // Customize the file name
  a.download = `detections_${Date.now()}.csv`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);

  ElMessage.success("CSV 已生成，下载中…");
};




</script>




<style scoped>
.control-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.control-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
}

.confidence-label {
  min-width: 70px;
  text-align: right;
  font-size: 14px;
  color: #606266;
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

.preview-media {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.content-table {
  margin-top: 40px;
  margin-bottom: 10vh;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.llm-analysis-section textarea {
  font-family: monospace;
  line-height: 1.5;
}


.control-panel {
  position: relative;
  width: 1480px !important;
  left: -15%;
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