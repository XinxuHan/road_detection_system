<template>
  <div>
    <el-card v-if="user">
      <el-descriptions class="margin-top" title="Introduction" :column="2" border>
        <!-- avatar -->
        <el-descriptions-item>
          <template #label>
            <el-icon ><PictureFilled /></el-icon>
            avatar
          </template>
          <img
              v-if="avatarUrl "
              class="img"
              :src="avatarUrl"
              alt="User Avatar"
          />
        </el-descriptions-item>

        <el-descriptions-item>
          <template #label>
            <el-icon><User /></el-icon>
            account
          </template>
          {{ user.account || 'Not set' }}
        </el-descriptions-item>

        <!-- Nick name -->
        <el-descriptions-item>
          <template #label>
            <el-icon><UserFilled /></el-icon>
            Nick name
          </template>
          {{ user.nick_name || 'No nickname set' }}
        </el-descriptions-item>

        <!-- age -->
        <el-descriptions-item>
          <template #label>
            <el-icon><Odometer /></el-icon>
            age
          </template>
          {{ user.age || 'Not set' }}
        </el-descriptions-item>

        <!-- 性别 -->
        <el-descriptions-item>
          <template #label>
            <el-icon>
              <Female v-if="user.gender === '0'" />
              <Male v-else-if="user.gender === '1'" />
              <User v-else />
            </el-icon>
            性别
          </template>
          <el-tag
              size="small"
              :type="user.gender === '0' ? 'danger' : user.gender === '1' ? 'primary' : 'info'"
          >
            {{ genderText  }}
          </el-tag>
        </el-descriptions-item>

        <!-- 邮箱 -->
        <el-descriptions-item>
          <template #label>
            <el-icon><Message /></el-icon>
            邮箱
          </template>
          {{ user.email || '未设置' }}
        </el-descriptions-item>

        <!-- 手机号码 -->
        <el-descriptions-item>
          <template #label>
            <el-icon><Phone /></el-icon>
            手机号码
          </template>
          {{ user.phone || '未设置' }}
        </el-descriptions-item>

        <!-- 注册日期 -->
        <el-descriptions-item>
          <template #label>
            <el-icon><Calendar /></el-icon>
            注册日期
          </template>
          {{ registerDate || '未知' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-empty v-else description="未找到用户信息" />
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from "vue";
import {
  PictureFilled,
  User,
  UserFilled,
  Odometer,
  Female,
  Male,
  Message,
  Phone,
  Calendar
} from "@element-plus/icons-vue";
import { useLoginUserStore } from "@/store/useLoginUserStore";
import myApi from "@/utils/request";

const userStore = useLoginUserStore();


const user = computed(() => ({
  account: '',
  nick_name: '',
  avatar: '',
  email: '',
  phone: '',
  gender: '',
  age: 0,
  addtime: '',
  ...userStore.loginUser
}));



const registerDate = computed(() => {
  if (!user.value.addtime) return "未提供";
  const date = new Date(user.value.addtime);
  return date.toISOString().split("T")[0];
});


const avatarUrl = computed(() => {
  if (!user.value.avatar) return null;
  return `${myApi.defaults.baseURL}/user/media/avatar/${user.value.avatar}?${Date.now()}`;
});

const genderText = computed(() => {
  if (user.value.gender === '1') return "男";
  if (user.value.gender === '0') return "女";
  return "未设置";
});



</script>

<style scoped>
.img {
  width: 80px;
  height: 80px;
}



</style>