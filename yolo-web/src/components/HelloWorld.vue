<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Recognition System</h1>
        <p  class="hero-subtitle">Suitable for object detection, segmentation and key point detection models, etc.</p>
        <el-button
            type="primary"
            size="large"
            round
            class="cta-button"
            @click="handleExplore"
        >
          get started
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleExplore = () => {

  router.push('/detect')


}
</script>

<style scoped>
.home-container {
  height: 80vh;
  overflow: hidden;
}

.hero-section {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 1.5s ease-in;
}

.hero-content {
  text-align: center;
  color: #3a710e;
  max-width: 700px;
  padding: 0 20px;
}

.hero-title {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2.5rem;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
}

.cta-button {
  padding: 1rem 2.5rem;
  font-size: 1.2rem;
  letter-spacing: 1px;
  transition: transform 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-3px);
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 移动端适配 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    color: #67C23A;
  }

  .cta-button {
    padding: 0.8rem 1.8rem;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }
}
</style>