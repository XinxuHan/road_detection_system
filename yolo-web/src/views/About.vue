<template>
  <div class="about-container">
    <div class="about-content">
      <h1 class="title">System Introduction</h1>
      <p class="version">Final Version</p>

      <section class="section">
        <h2>System Introduction</h2>
        <p>
          This project presents an <strong>Unstructured Road Drivable Area Identification Platform</strong>, developed using the <strong>Django + Vue3</strong> technology stack. It aims to provide <strong>real-time semantic segmentation and obstacle detection</strong> for complex road environments, particularly focusing on unstructured scenarios.
          <br><br>
          By integrating an enhanced version of the <strong>YOLOv11/v8 segmentation model</strong> in the backend and a responsive front-end user interface, the system can accurately identify <strong>drivable areas</strong> and <strong>non-drivable obstacles</strong>, supporting key applications in <em>autonomous driving</em>, <em>infrastructure inspection</em>, and <em>traffic safety monitoring</em>.
          <br><br>
          The system architecture follows a <strong>front-end and back-end decoupled design</strong>. The frontend is built with <strong>Vue3 + Element Plus</strong>, offering a highly interactive and user-friendly interface. The backend is developed with <strong>Django</strong>, providing robust <strong>RESTful APIs</strong> and optional <strong>WebSocket</strong> support to ensure real-time streaming, segmentation, and feedback of detection results.
          <br><br>
          The system supports <strong>multi-modal input</strong>, <strong>dynamic model configuration</strong>, and <strong>flexible model management</strong>, enabling rapid deployment and testing of diverse perception scenarios.
        </p>
      </section>

      <section class="section">
        <h2>Core Features</h2>
        <ul>
          <li>✅ User login and registration with secure backend validation</li>
          <li>✅ Modular model switching for YOLOv11/v8 variants</li>
          <li>✅ Custom model replacement support</li>
          <li>✅ Video stream analysis (supports MP4/AVI format, real-time processing)</li>
          <li>✅ Static image detection (supports JPG/PNG/BMP formats)</li>
          <li>✅ Adjustable detection parameters (confidence, IoU threshold)</li>
          <li>✅ Structured result visualization (real-time result display in table)</li>
          <li>✅ Optional LLM analysis with Zero-shot, Few-shot, and CoT reasoning</li>
        </ul>
      </section>

      <section class="section">
        <h2>Technology Stack</h2>
        <p><strong>Back-end:</strong> Django Framework, YOLOv11/v8 Segmentation Model</p>
        <p><strong>Front-end:</strong> Vue3, Element Plus, Pinia</p>
        <p><strong>Communication:</strong> RESTful API, WebSocket (optional)</p>
        <p><strong>Development Tools:</strong> PyCharm, WebStorm, Anaconda3, Node.js, MySQL</p>
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
