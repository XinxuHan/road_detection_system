<!--<template>-->
<!--  <div>-->
<!--    <el-card v-if="user">-->
<!--      <el-descriptions class="margin-top" title="简介" :column="2" border>-->
<!--        &lt;!&ndash; 头像 &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon ><PictureFilled /></el-icon>-->
<!--            头像-->
<!--          </template>-->
<!--          <img-->
<!--              v-if="avatarUrl "-->
<!--              class="img"-->
<!--              :src="avatarUrl"-->
<!--              alt="用户头像"-->
<!--          />-->
<!--        </el-descriptions-item>-->

<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><User /></el-icon>-->
<!--            账号-->
<!--          </template>-->
<!--          {{ user.account || '未设置' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; 昵称 &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><UserFilled /></el-icon>-->
<!--            昵称-->
<!--          </template>-->
<!--          {{ user.nick_name || '未设置昵称' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; 年龄 &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><Odometer /></el-icon>-->
<!--            年龄-->
<!--          </template>-->
<!--          {{ user.age || '未设置' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; 性别 &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon>-->
<!--              <Female v-if="user.gender === '0'" />-->
<!--              <Male v-else-if="user.gender === '1'" />-->
<!--              <User v-else />-->
<!--            </el-icon>-->
<!--            性别-->
<!--          </template>-->
<!--          <el-tag-->
<!--              size="small"-->
<!--              :type="user.gender === '0' ? 'danger' : user.gender === '1' ? 'primary' : 'info'"-->
<!--          >-->
<!--            {{ genderText  }}-->
<!--          </el-tag>-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; 邮箱 &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><Message /></el-icon>-->
<!--            邮箱-->
<!--          </template>-->
<!--          {{ user.email || '未设置' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; 手机号码 &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><Phone /></el-icon>-->
<!--            手机号码-->
<!--          </template>-->
<!--          {{ user.phone || '未设置' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; 注册日期 &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><Calendar /></el-icon>-->
<!--            注册日期-->
<!--          </template>-->
<!--          {{ registerDate || '未知' }}-->
<!--        </el-descriptions-item>-->
<!--      </el-descriptions>-->
<!--    </el-card>-->

<!--    <el-empty v-else description="未找到用户信息" />-->
<!--  </div>-->
<!--</template>-->

<!--<script setup lang="ts">-->
<!--import {computed, ref} from "vue";-->
<!--import {-->
<!--  PictureFilled,-->
<!--  User,-->
<!--  UserFilled,-->
<!--  Odometer,-->
<!--  Female,-->
<!--  Male,-->
<!--  Message,-->
<!--  Phone,-->
<!--  Calendar-->
<!--} from "@element-plus/icons-vue";-->
<!--import { useLoginUserStore } from "@/store/useLoginUserStore";-->
<!--import myApi from "@/utils/request";-->

<!--const userStore = useLoginUserStore();-->


<!--const user = computed(() => ({-->
<!--  account: '',-->
<!--  nick_name: '',-->
<!--  avatar: '',-->
<!--  email: '',-->
<!--  phone: '',-->
<!--  gender: '',-->
<!--  age: 0,-->
<!--  addtime: '',-->
<!--  ...userStore.loginUser-->
<!--}));-->



<!--const registerDate = computed(() => {-->
<!--  if (!user.value.addtime) return "未提供";-->
<!--  const date = new Date(user.value.addtime);-->
<!--  return date.toISOString().split("T")[0];-->
<!--});-->


<!--const avatarUrl = computed(() => {-->
<!--  if (!user.value.avatar) return null;-->
<!--  return `${myApi.defaults.baseURL}/user/media/avatar/${user.value.avatar}?${Date.now()}`;-->
<!--});-->

<!--const genderText = computed(() => {-->
<!--  if (user.value.gender === '1') return "男";-->
<!--  if (user.value.gender === '0') return "女";-->
<!--  return "未设置";-->
<!--});-->



<!--</script>-->

<!--<style scoped>-->
<!--.img {-->
<!--  width: 80px;-->
<!--  height: 80px;-->
<!--}-->



<!--</style>-->