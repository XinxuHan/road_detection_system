<template>
  <div class="register-page">
    <div class="register-container">
      <h1 class="register-title">User Registration</h1>
      <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>
      <form @submit.prevent="handleSubmit" class="form">
        <el-form-item label="Account" required>
          <el-input v-model="form.account" placeholder="Please enter your account" clearable />
          <div v-if="errors.account" class="field-error">{{ errors.account }}</div>
        </el-form-item>

        <el-form-item label="Password" required>
          <el-input v-model="form.password" type="password" placeholder="Please enter your password" show-password clearable />
          <div v-if="errors.password" class="field-error">{{ errors.password }}</div>
        </el-form-item>

        <el-form-item label="Confirm Password" required>
          <el-input v-model="form.checkPassword" type="password" placeholder="Please confirm your password" show-password clearable />
          <div v-if="errors.checkPassword" class="field-error">{{ errors.checkPassword }}</div>
        </el-form-item>

        <el-form-item label="Phone number" required>
          <el-input v-model="form.phone" placeholder="Please enter your phone number" clearable />
          <div v-if="errors.phone" class="field-error">{{ errors.phone }}</div>
        </el-form-item>

        <el-form-item label="Email" required>
          <el-input v-model="form.email" placeholder="Please enter your email" clearable />
          <div v-if="errors.email" class="field-error">{{ errors.email }}</div>
        </el-form-item>

        <el-button type="primary" class="register-btn" :loading="loading" native-type="submit">Register</el-button>

        <div class="login-link">
          Already have an account?<router-link to="/login">Sign in now</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/login/user'

const errorMessage = ref('')
const form = ref({
  account: '',
  password: '',
  checkPassword: '',
  phone: '',
  email: ''
})
const errors = ref<any>({})
const loading = ref(false)
const router = useRouter()
const accountRegExp = /^[a-zA-Z0-9_]+$/

const handleSubmit = async () => {
  errors.value = {}
  if (!accountRegExp.test(form.value.account)) {
    errors.value.account = '账号只能包含字母、数字和下划线'
    return
  }
  if (form.value.password !== form.value.checkPassword) {
    errors.value.checkPassword = '密码和确认密码不一致'
    return
  }
  loading.value = true
  errorMessage.value = ''
  try {
    const response = await register(form.value)
    if (response.data.success) {
      router.push('/login')
    } else {
      errors.value = response.data.errors || {}
    }
  } catch (e) {
    errorMessage.value = '注册失败，请稍后再试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: calc(100vh - 64px);
  background: url('@/assets/home-bg.jpg') center/cover no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 500px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 40px 36px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(220, 220, 220, 0.5);
}

.register-title {
  text-align: center;
  font-size: 26px;
  font-weight: bold;
  color: #4687f5;
  margin-bottom: 24px;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field-error {
  color: #e74c3c;
  font-size: 13px;
  margin-top: 4px;
}

.register-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
  box-shadow: 0 4px 14px rgba(70, 135, 245, 0.2);
  transition: transform 0.2s ease;
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(70, 135, 245, 0.3);
}

.login-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #888;
}
.login-link a {
  color: #4687f5;
  font-weight: 500;
  margin-left: 4px;
  text-decoration: none;
}
.login-link a:hover {
  text-decoration: underline;
}

.error-msg {
  color: #e74c3c;
  text-align: center;
  margin-bottom: 12px;
  font-size: 15px;
  font-weight: 500;
}
</style>
