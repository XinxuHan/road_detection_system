<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Recognition System</h1>
        <p  class="hero-subtitle">Deep Learning Based Recognition System for Unstructured Road-Drivable Areas</p>
        <el-button
            type="primary"
            size="large"
            round
            class="cta-button"
            @click="handleExplore"
        >
          Start
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
  height: calc(100vh - 64px); /* Assuming header is 64px */
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url('@/assets/home-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.hero-section {
  text-align: center;
  animation: fadeIn 1.5s ease-in;
  z-index: 1;
}

.hero-content {
  max-width: 700px;
  padding: 0 20px;
  color: #fff;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
}

.hero-title {
  font-size: 3.2rem;
  margin-bottom: 1.5rem;
  color: #ffffff;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 1.4rem;
  color: #e0e0e0;
  margin-bottom: 2rem;
}

.cta-button {
  padding: 1rem 2.5rem;
  font-size: 1.2rem;
  background-color: #4687f5;
  border: none;
  box-shadow: 0 4px 12px rgba(70, 135, 245, 0.3);
  font-weight: 500;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #3c75e1;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(70, 135, 245, 0.4);
}

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

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  .hero-subtitle {
    font-size: 1.2rem;
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
