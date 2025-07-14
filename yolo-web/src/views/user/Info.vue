<template>
  <div>
    <el-card v-if="user">
      <el-descriptions
        class="margin-top"
        title="User Profile"
        :column="2"
        border
      >
        <!-- avatar -->
        <el-descriptions-item>
          <template #label>
            <el-icon><PictureFilled /></el-icon>
            Avatar
          </template>
          <img
            v-if="avatarUrl"
            class="img"
            :src="avatarUrl"
            alt="User Avatar"
          />
        </el-descriptions-item>

        <!-- account -->
        <el-descriptions-item>
          <template #label>
            <el-icon><User /></el-icon>
            Account
          </template>
          {{ user.account ?? 'Not set' }}
        </el-descriptions-item>

        <!-- nickname -->
        <el-descriptions-item>
          <template #label>
            <el-icon><UserFilled /></el-icon>
            Nickname
          </template>
          {{ user.nick_name ?? 'No nickname' }}
        </el-descriptions-item>

        <!-- age -->
        <el-descriptions-item>
          <template #label>
            <el-icon><Odometer /></el-icon>
            Age
          </template>
          {{ user.age || 'Unknown' }}
        </el-descriptions-item>

        <!-- gender -->
        <el-descriptions-item>
          <template #label>
            <el-icon>
              <template v-if="user.gender === '0'"><Female /></template>
              <template v-else-if="user.gender === '1'"><Male /></template>
              <template v-else><User /></template>
            </el-icon>
            Gender
          </template>
          <el-tag
            size="small"
            :type="user.gender === '0' ? 'danger' : user.gender === '1' ? 'primary' : 'info'"
          >
            {{ genderText }}
          </el-tag>
        </el-descriptions-item>

        <!-- email -->
        <el-descriptions-item>
          <template #label>
            <el-icon><Message /></el-icon>
            Email
          </template>
          {{ user.email ?? 'Not provided' }}
        </el-descriptions-item>

        <!-- phone -->
        <el-descriptions-item>
          <template #label>
            <el-icon><Phone /></el-icon>
            Phone
          </template>
          {{ user.phone ?? 'Not provided' }}
        </el-descriptions-item>

        <!-- registration date -->
        <el-descriptions-item>
          <template #label>
            <el-icon><Calendar /></el-icon>
            Registered
          </template>
          {{ formattedRegisterDate }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-empty v-else description="No user data found" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
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
} from '@element-plus/icons-vue'
import { useLoginUserStore } from '@/store/useLoginUserStore'
import myApi from '@/utils/request'

const store = useLoginUserStore()

const user = computed(() => ({
  account: '',
  nick_name: '',
  avatar: '',
  email: '',
  phone: '',
  gender: '',
  age: 0,
  addtime: '',
  ...store.loginUser
}))

const formattedRegisterDate = computed(() => {
  const raw = user.value.addtime
  if (!raw) return 'Not provided'
  const date = new Date(raw)
  return date.toLocaleDateString('en-CA') // format: YYYY-MM-DD
})

const avatarUrl = computed(() => {
  const avatar = user.value.avatar
  return avatar ? `${myApi.defaults.baseURL}/user/media/avatar/${avatar}?t=${Date.now()}` : null
})

const genderText = computed(() => {
  const gender = user.value.gender
  return gender === '1' ? 'Male' : gender === '0' ? 'Female' : 'Not set'
})
</script>

<style scoped>
.img {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  object-fit: cover;
}
</style>
