<template>
  <el-dialog :model-value="dialogVisible" title="Modify personal information" width="50%" @close="handleClose">
    <el-form  :model="form" label-width="150px">

      <div class="updateinfo">

        <div class="left">
          <el-form-item label="avatar" prop="avatar">
            <el-upload
                class="avatar-uploader"
                name="avatar"
                action="http://localhost:8000/api/upload-avatar/"
                :show-file-list="false"
                :on-success="handleAvatarSuccess">
              <img v-if="avatarUrl" :src="avatarUrl" class="avatar" />
              <el-icon v-else class="avatar-uploader-icon"></el-icon>
            </el-upload>
            <!--            <img style="width:150px;height:110px" :src="userInfo.avatarUrl" />-->
          </el-form-item>
          <el-form-item label="Nick name" prop="nick_name">

            <el-input v-model="form.nick_name" />
          </el-form-item>
          <el-form-item label="age" prop="age">
            <el-input v-model="form.age" :min="0" :max="120"></el-input>
          </el-form-item>
          <el-form-item label="gender" prop="gender">
            <el-switch
                v-model="form.gender"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="Male"
                inactive-text="Female"
                :active-value= "'1'"
                :inactive-value= "'0'"
            >
            </el-switch>
          </el-form-item>


        </div>

        <div class="right">
          <el-form-item label="account" prop="account">
            <el-input v-model="form.account" disabled></el-input>
          </el-form-item>
          <el-form-item label="Email" prop="email">
            <el-input v-model="form.email"></el-input>
          </el-form-item>
          <el-form-item label="phone number" prop="phone">
            <el-input v-model="form.phone"></el-input>
          </el-form-item>
        </div>



      </div>


    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button type="primary"  @click="handleSubmit">submit</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import {computed, defineEmits, onMounted, reactive, ref, watch} from 'vue';
import {useUserInfo} from "@/utils/userinfo";
import {useLoginUserStore} from "@/store/useLoginUserStore";
import {updateUser} from "@/api/login/user";
import {ElMessage, ElNotification ,ElForm} from "element-plus";
import type { UploadProps } from 'element-plus'
import myApi from "@/utils/request";
// Send dialogVisible changes via emits
const emits = defineEmits(["update:modelValue"]);
const dialogVisible = ref<boolean>(false);


// Form Data
const form = reactive({
  account:"",
  avatar: "",
  nick_name: "",
  gender: "",
  email: "",
  age: 0 ,
  phone:"",
});


const loginUserStore = useLoginUserStore();

const user = loginUserStore.loginUser;


const avatarUrl =ref("")


// Loading user information
onMounted(() => {
  if (user) {
    form.nick_name = user.nick_name;
    form.account = user.account;
    form.email = user.email;
    form.phone = user.phone;
    form.age = user.age;
    form.gender = user.gender;
    form.avatar = user.avatar;
    avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${user.avatar}`;
  }


});


// Upload avatar
const handleAvatarSuccess = (res: any) => {
  console.log(res);
  avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${res.avatarUrl}`;
  form.avatar = res.avatarUrl;  // Save the file name to form.avatar and submit it together when submitting
}



// Synchronize UI after updating data
const handleSubmit = async () => {
  try {
    const formData = new FormData();
    formData.append('nick_name', form.nick_name);
    formData.append('email', form.email);
    formData.append('phone', form.phone);
    formData.append('age', String(form.age));
    formData.append('gender', form.gender);
    if (form.avatar) formData.append('avatar', form.avatar);  // If the user has uploaded an avatar, add it to FormData

    await updateUser(formData);  // Call the backend API to update user information

    // Update user data in Pinia store
    loginUserStore.setLoginUser({
      ...loginUserStore.loginUser,
      ...form,
    });

    emits('update:modelValue', false);  // Close dialog box

    ElMessage({
      message: 'User information updated successfully',
      type: 'success',
    })

  } catch (error) {
    ElNotification({
      title: 'Warning',
      message: 'The server is busy, please try again later',
      type: 'warning',
    })
  }
};


const handleClose = () => {
  //Click Cancel to restore the form data to the latest user data
  form.nick_name = loginUserStore.loginUser.nick_name;
  form.account = loginUserStore.loginUser.account;
  form.email = loginUserStore.loginUser.email;
  form.phone = loginUserStore.loginUser.phone;
  form.age = loginUserStore.loginUser.age;
  form.gender = loginUserStore.loginUser.gender;
  avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${loginUserStore.loginUser.avatar}`;

  emits("update:modelValue", false);
};




</script>
<style scoped>
.updateinfo {
  height: 350px;
  overflow: auto;
}
.left {
  width: 330px;
  float: left;
  padding: 0;

}
.right {
  width: 400px;
  overflow: hidden;
}

/* Use :deep() to cover the border of el-input */
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