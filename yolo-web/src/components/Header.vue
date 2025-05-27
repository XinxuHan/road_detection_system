<template>
  <div class="header-layout">
    <!-- Logo + Title -->
    <div class="logo">
      <img class="logo-img" src="@/assets/logo.svg" alt="logo" />
      <div class="title">Recognition system based on YOLOv11</div>
    </div>

    <!-- 导航菜单整体居中容器 -->
    <div class="nav-container">
      <nav class="nav-menu" v-show="!menuVisibleOnMobile">
        <RouterLink to="/hello" active-class="router-link-active">首页</RouterLink>
        <RouterLink to="/detect" active-class="router-link-active">检测程序</RouterLink>
        <RouterLink to="/user/center" active-class="router-link-active">个人中心</RouterLink>
        <RouterLink to="/about" active-class="router-link-active">关于</RouterLink>
      </nav>
    </div>

    <!-- 用户信息 / 登录注册 -->
    <div class="user-area">
      <div v-if="loginUserStore.loginUser" class="avatar-show">
        <el-avatar :src="avatarUrl" class="avatar" />
        <el-dropdown>
          <span class="el-dropdown-link">
            {{ loginUserStore.loginUser.nick_name }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
      <div v-else class="header-right">
        <RouterLink to="/login" class="auth-link">登录</RouterLink>
        <span class="divider">｜</span>
        <RouterLink to="/register" class="auth-link">注册</RouterLink>
      </div>
    </div>

    <!-- 移动端菜单按钮 -->
    <div class="hamburger" @click="menuVisibleOnMobile = !menuVisibleOnMobile">
      <span></span><span></span><span></span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useLoginUserStore } from '@/store/useLoginUserStore'
import { ArrowDown } from '@element-plus/icons-vue'
import myApi from '@/utils/request'

const loginUserStore = useLoginUserStore()
const router = useRouter()
const menuVisibleOnMobile = ref(false)
const avatarUrl = ref('')

watchEffect(() => {
  avatarUrl.value = loginUserStore.loginUser?.avatar
      ? `${myApi.defaults.baseURL}/user/media/avatar/${loginUserStore.loginUser.avatar}`
      : new URL('@/assets/default-avatar.png', import.meta.url).href
})

const logout = () => {
  loginUserStore.clearLoginUser()
  router.push({ path: '/hello', replace: true })
}
</script>

<style scoped>
.header-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 64px;
  background-color: #ffffff;
  border-bottom: 1px solid #eee;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.logo {
  display: flex;
  align-items: center;
}
.logo-img {
  height: 160px;
  margin-right: 12px;
}
.title {
  font-size: 18px;
  font-weight: 600;
  color: #4687f5;
}

.nav-container {
  flex: 1;
  display: flex;
  justify-content: center;
}
.nav-menu {
  display: flex;
  gap: 36px;
  font-size: 15px;
}
.nav-menu a {
  color: #333;
  text-decoration: none;
  padding-bottom: 4px;
  transition: all 0.2s;
}
.nav-menu a:hover,
.router-link-active {
  color: #4687f5;
  border-bottom: 2px solid #4687f5;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 16px;
}
.avatar-show {
  display: flex;
  align-items: center;
  gap: 8px;
}
.avatar {
  border-radius: 50%;
  width: 36px;
  height: 36px;
  object-fit: cover;
  border: 2px solid #4687f5;
  transition: box-shadow 0.3s;
}
.avatar:hover {
  box-shadow: 0 0 8px rgba(70, 135, 245, 0.6);
}
.el-dropdown-link {
  cursor: pointer;
  color: #4687f5;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.header-right {
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.auth-link {
  color: #c0392b;
  font-weight: 500;
  transition: color 0.2s;
}
.auth-link:hover {
  color: #e74c3c;
  text-decoration: underline;
}
.divider {
  color: #ddd;
  font-size: 16px;
}

.hamburger {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  height: 16px;
  cursor: pointer;
}
.hamburger span {
  height: 2px;
  width: 20px;
  background-color: #4687f5;
  border-radius: 1px;
}

@media screen and (max-width: 768px) {
  .nav-menu {
    display: none;
  }
  .hamburger {
    display: flex;
  }
}
</style>
