<template>
  <div class="about-container">
    <div class="about-content">
      <h1 class="title">基于 Web 的 YOLOv11 目标检测系统</h1>
      <p class="version">Version 1.0.0</p>

      <section class="section">
        <h2>系统简介</h2>
        <p>
          本系统是一套基于 Django + Vue3 技术栈开发的“非结构化道路可行驶区域识别平台”，旨在通过深度学习算法实现复杂道路场景下的实时分割与可视化识别。系统后端集成了改进版 YOLOv11语义分割模型，结合前端交互界面，能够高效识别非结构化道路中的可行驶区域与障碍物，广泛适用于自动驾驶、道路巡检及交通安全等场景。

          系统采用前后端分离架构，前端使用 Vue3 + Element Plus 构建响应式交互界面，后端基于 Django 实现 RESTful API 和 WebSocket 通信，保障实时视频流的处理和分割结果的回传。系统支持图片/视频输入、模型参数调节（如置信度和IoU阈值）、实时检测结果展示与多模型快速切换。
        </p>
      </section>

      <section class="section">
        <h2>核心功能</h2>
        <ul>
          <li>✅ 用户登录和注册</li>
          <li>✅ 支持 YOLOv11 模型快速替换</li>
          <li>✅ 更换自己的模型</li>
          <li>✅ 视频流处理（支持 MP4/AVI 格式，实时帧处理与结果回显）</li>
          <li>✅ 图像检测（支持 JPG/PNG/BMP 格式）</li>
          <li>✅ 参数调节（置信度调节，IoU 参数调节）</li>
          <li>✅ 结果展示（表格形式直观显示检测结果）</li>
        </ul>
      </section>

      <section class="section">
        <h2>技术</h2>
        <p><strong>后端：</strong>Django 框架 + YOLOv11 目标检测算法</p>
        <p><strong>前端：</strong>Vue3 + Element Plus + Pinia 等技术</p>
        <p><strong>开发工具：</strong>PyCharm、WebStorm、Anaconda3、Node、MySQL 等</p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.about-container {
  max-width: 900px;
  margin: 60px auto;
  padding: 0 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

.about-content {
  background: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 28px;
  font-weight: bold;
  color: #4687f5;
  margin-bottom: 10px;
}

.version {
  font-size: 14px;
  color: #888;
  margin-bottom: 30px;
}

.section {
  margin-bottom: 36px;
}

.section h2 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #222;
}

.section p {
  font-size: 15px;
  line-height: 1.8;
}

.section ul {
  padding-left: 20px;
  font-size: 15px;
  line-height: 2;
}

.section li::marker {
  color: #4687f5;
}
</style>
