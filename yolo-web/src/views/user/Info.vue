<!--<template>-->
<!--  <div>-->
<!--    <el-card v-if="user">-->
<!--      <el-descriptions class="margin-top" title="Introduction" :column="2" border>-->
<!--        &lt;!&ndash; avatar &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon ><PictureFilled /></el-icon>-->
<!--            avatar-->
<!--          </template>-->
<!--          <img-->
<!--              v-if="avatarUrl "-->
<!--              class="img"-->
<!--              :src="avatarUrl"-->
<!--              alt="User Avatar"-->
<!--          />-->
<!--        </el-descriptions-item>-->

<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><User /></el-icon>-->
<!--            account-->
<!--          </template>-->
<!--          {{ user.account || 'Not set' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; Nick name &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><UserFilled /></el-icon>-->
<!--            Nick name-->
<!--          </template>-->
<!--          {{ user.nick_name || 'No nickname set' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; age &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><Odometer /></el-icon>-->
<!--            age-->
<!--          </template>-->
<!--          {{ user.age || 'Not set' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; gender &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon>-->
<!--              <Female v-if="user.gender === '0'" />-->
<!--              <Male v-else-if="user.gender === '1'" />-->
<!--              <User v-else />-->
<!--            </el-icon>-->
<!--            gender-->
<!--          </template>-->
<!--          <el-tag-->
<!--              size="small"-->
<!--              :type="user.gender === '0' ? 'danger' : user.gender === '1' ? 'primary' : 'info'"-->
<!--          >-->
<!--            {{ genderText  }}-->
<!--          </el-tag>-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; Email &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><Message /></el-icon>-->
<!--            Email-->
<!--          </template>-->
<!--          {{ user.email || 'Not set' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; phone number &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><Phone /></el-icon>-->
<!--            phone number-->
<!--          </template>-->
<!--          {{ user.phone || 'Not set' }}-->
<!--        </el-descriptions-item>-->

<!--        &lt;!&ndash; Registration Date &ndash;&gt;-->
<!--        <el-descriptions-item>-->
<!--          <template #label>-->
<!--            <el-icon><Calendar /></el-icon>-->
<!--            Registration Date-->
<!--          </template>-->
<!--          {{ registerDate || 'unknown' }}-->
<!--        </el-descriptions-item>-->
<!--      </el-descriptions>-->
<!--    </el-card>-->

<!--    <el-empty v-else description="User information not found" />-->
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
<!--  if (!user.value.addtime) return "Not provided";-->
<!--  const date = new Date(user.value.addtime);-->
<!--  return date.toISOString().split("T")[0];-->
<!--});-->


<!--const avatarUrl = computed(() => {-->
<!--  if (!user.value.avatar) return null;-->
<!--  return `${myApi.defaults.baseURL}/user/media/avatar/${user.value.avatar}?${Date.now()}`;-->
<!--});-->

<!--const genderText = computed(() => {-->
<!--  if (user.value.gender === '1') return "Male";-->
<!--  if (user.value.gender === '0') return "Female";-->
<!--  return "Not Set";-->
<!--});-->



<!--</script>-->

<!--<style scoped>-->
<!--.img {-->
<!--  width: 80px;-->
<!--  height: 80px;-->
<!--}-->



<!--</style>-->