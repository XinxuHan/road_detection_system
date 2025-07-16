<template>
  <el-dialog
    :model-value="visibleDialog"
    title="Modify personal information"
    width="50%"
    @close="closeDialog"
  >
    <el-form :model="formData" label-width="150px">
      <div class="info-wrapper">
        <div class="form-left">
          <el-form-item label="Avatar" prop="avatar">
            <el-upload
              class="avatar-uploader"
              name="avatar"
              :action="uploadEndpoint"
              :show-file-list="false"
              :on-success="onAvatarUpload"
            >
              <img v-if="avatarUrl" :src="avatarUrl" class="avatar" />
              <el-icon v-else class="avatar-uploader-icon" />
            </el-upload>
          </el-form-item>

          <el-form-item label="Name" prop="name">
            <el-input v-model="formData.name" />
          </el-form-item>

          <el-form-item label="Age" prop="age">
            <el-input v-model="formData.age" :min="0" :max="120" />
          </el-form-item>

          <el-form-item label="Gender" prop="gender">
            <el-switch
              v-model="formData.gender"
              active-color="#13ce66"
              inactive-color="#ff4949"
              active-text="Male"
              inactive-text="Female"
              :active-value="'1'"
              :inactive-value="'0'"
            />
          </el-form-item>
        </div>

        <div class="form-right">
          <el-form-item label="Account" prop="account">
            <el-input v-model="formData.account" disabled />
          </el-form-item>

          <el-form-item label="Email" prop="email">
            <el-input v-model="formData.email" />
          </el-form-item>

          <el-form-item label="Phone" prop="phone">
            <el-input v-model="formData.phone" />
          </el-form-item>
        </div>
      </div>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="closeDialog">Cancel</el-button>
        <el-button type="primary" @click="submitForm">Submit</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, defineEmits, computed } from 'vue';
import { useLoginUserStore } from '@/store/useLoginUserStore';
import { updateUser } from '@/api/login/user';
import { ElMessage, ElNotification } from 'element-plus';
import myApi from '@/utils/request';

const props = defineProps<{ modelValue: boolean }>();
const emits = defineEmits(['update:modelValue']);

const visibleDialog = computed({
  get: () => props.modelValue,
  set: val => emits('update:modelValue', val)
});

const formData = reactive({
  account: '',
  avatar: '',
  name: '',
  gender: '',
  email: '',
  age: 0,
  phone: ''
});

const loginUserStore = useLoginUserStore();
const currentUser = loginUserStore.loginUser;
const avatarUrl = ref('');
const uploadEndpoint = `${myApi.defaults.baseURL}/api/upload_avatar/`;

onMounted(() => {
  if (!currentUser) return;
  Object.assign(formData, currentUser);
  avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${currentUser.avatar}`;
});

const onAvatarUpload = (res: any) => {
  avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${res.avatarUrl}`;
  formData.avatar = res.avatarUrl;
};

const submitForm = async () => {
  try {
    const payload = new FormData();
    const keys = Object.keys(formData) as (keyof typeof formData)[];
    keys.forEach((key) => {
      const value = formData[key];
      if (value !== undefined && value !== null) {
        payload.append(key, String(value));
      }
    });

    await updateUser(payload);

    loginUserStore.setLoginUser({
      ...loginUserStore.loginUser,
      ...formData
    });

    emits('update:modelValue', false);
    ElMessage.success('User information updated successfully');
  } catch (err) {
    ElNotification({
      title: 'Warning',
      message: 'Failed to update user data. Please try again.',
      type: 'warning'
    });
  }
};

const closeDialog = () => {
  Object.assign(formData, loginUserStore.loginUser);
  avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${loginUserStore.loginUser.avatar}`;
  emits('update:modelValue', false);
};
</script>

<style scoped>
.info-wrapper {
  height: 350px;
  display: flex;
  gap: 20px;
}
.form-left {
  width: 330px;
}
.form-right {
  width: 400px;
}
:deep(.el-input__wrapper) {
  padding: 0 !important;
}
.avatar-uploader .avatar {
  width: 120px;
  height: 120px;
  display: block;
}
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}
.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}
.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>
