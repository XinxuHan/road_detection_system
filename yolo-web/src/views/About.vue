<template>
  <div class="about-container">
    <div class="about-content">
      <h1 class="title">System Introduction</h1>
      <p class="version">Version 1.0.0</p>

      <section class="section">
        <h2>System Introduction</h2>
        <p>
          This system is a "unstructured road drivable area identification platform" developed based on the Django + Vue3 technology stack, which aims to achieve real-time segmentation and visual identification in complex road scenes through deep learning algorithms. The system backend integrates an improved version of the YOLOv11 semantic segmentation model, combined with the front-end interactive interface, which can efficiently identify drivable areas and obstacles in unstructured roads, and is widely used in scenarios such as autonomous driving, road inspections, and traffic safety.
          The system adopts a front-end and back-end separation architecture. The front-end uses Vue3 + Element Plus to build a responsive interactive interface, and the back-end implements RESTful API and WebSocket communication based on Django to ensure the processing of real-time video streams and the return of segmentation results. The system supports image/video input, model parameter adjustment (such as confidence and IoU threshold), real-time detection result display, and fast switching of multiple models.
        </p>
      </section>

      <section class="section">
        <h2>Core Features</h2>
        <ul>
          <li>✅ User Login and Registration</li>
          <li>✅ Support fast replacement of YOLOv11 model</li>
          <li>✅ Replace your own model</li>
          <li>✅ Video stream processing (support MP4/AVI format, real-time frame processing and result display)</li>
          <li>✅ Image detection (support JPG/PNG/BMP formats)</li>
          <li>✅ Parameter adjustment (confidence adjustment, IoU parameter adjustment)</li>
          <li>✅ Result display (intuitive display of test results in table form)</li>
        </ul>
      </section>

      <section class="section">
        <h2>technology</h2>
        <p><strong>back-end:</strong>Django framework + YOLOv11 target detection algorithm</p>
        <p><strong>front end:</strong>Vue3 + Element Plus + Pinia and other technologies</p>
        <p><strong>Development Tools:</strong>PyCharm、WebStorm、Anaconda3、Node、MySQL and so on</p>
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
