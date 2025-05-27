<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <div class="page-header">
          <h1 class="login-title">User Login</h1>
        </div>

        <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>

        <form @submit.prevent="handleSubmit" class="form">
          <el-form-item label="Account" required>
            <el-input v-model="form.account" placeholder="Please enter your account" clearable />
          </el-form-item>

          <el-form-item label="Password" required>
            <el-input v-model="form.password" type="password" placeholder="Please enter your password" show-password clearable />
          </el-form-item>

          <el-button type="primary" :loading="loading" class="login-btn" native-type="submit">Login</el-button>

          <div class="register-link">
            No account?<router-link to="/register">Register Now</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/login/user'
import { useLoginUserStore } from '@/store/useLoginUserStore'

const form = ref({ account: '', password: '' })
const loading = ref(false)
const errorMessage = ref('')
const router = useRouter()
const loginUserStore = useLoginUserStore()

const handleSubmit = async () => {
  loading.value = true
  errorMessage.value = ''
  try {
    const response = await login({ account: form.value.account, password: form.value.password })
    if (response.data.success) {
      loginUserStore.setLoginUser(response.data.user)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      router.push('/')
    } else {
      errorMessage.value = response.data.error
    }
  } catch (e) {
    errorMessage.value = 'The system is busy, please try again later!'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 64px);
  background: url('@/assets/home-bg.jpg') center/cover no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 500px;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  padding: 48px 36px;
  position: relative;
  transition: all 0.4s ease-in-out;
  border: 1px solid rgba(200, 200, 200, 0.3);
}

.login-title {
  font-size: 26px;
  font-weight: 700;
  color: #4687f5;
  text-align: center;
  margin-bottom: 28px;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.el-input {
  font-size: 8px;
  border-radius: 8px;
}

.login-btn {
  width: 100%;
  height: 36px;
  font-size: 16px;
  border-radius: 10px;
  font-weight: 500;
  box-shadow: 0 4px 14px rgba(70, 135, 245, 0.3);
  transition: transform 0.2s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(70, 135, 245, 0.4);
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #999;
  font-size: 14px;
}

.register-link a {
  color: #4687f5;
  font-weight: 500;
  margin-left: 4px;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

.error-msg {
  color: #e74c3c;
  text-align: center;
  margin-bottom: 10px;
  font-size: 15px;
  font-weight: 500;
}
</style>
