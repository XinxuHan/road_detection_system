<template>
  <el-dialog :model-value="dialogVisible" title="修改个人信息" width="50%" @close="handleClose">
    <el-form  :model="form" label-width="150px">

      <div class="updateinfo">

        <div class="left">
          <el-form-item label="头像" prop="avatar">
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
          <el-form-item label="昵称" prop="nick_name">

            <el-input v-model="form.nick_name" />
          </el-form-item>
          <el-form-item label="年龄" prop="age">
            <el-input v-model="form.age" :min="0" :max="120"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-switch
                v-model="form.gender"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="男"
                inactive-text="女"
                :active-value= "'1'"
                :inactive-value= "'0'"
            >
            </el-switch>
          </el-form-item>


        </div>

        <div class="right">
          <el-form-item label="账号" prop="account">
            <el-input v-model="form.account" disabled></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="form.email"></el-input>
          </el-form-item>
          <el-form-item label="手机号码" prop="phone">
            <el-input v-model="form.phone"></el-input>
          </el-form-item>
        </div>



      </div>


    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary"  @click="handleSubmit">提交</el-button>
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
// 通过 emits 发送 dialogVisible 的变化
const emits = defineEmits(["update:modelValue"]);
const dialogVisible = ref<boolean>(false);


// 表单数据
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


// 加载用户信息
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


// 头像上传
const handleAvatarSuccess = (res: any) => {
  console.log(res);
  avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${res.avatarUrl}`;
  form.avatar = res.avatarUrl;  // 将文件名保存到form.avatar，提交时一起提交
}



// 更新数据后同步 UI
const handleSubmit = async () => {
  try {
    const formData = new FormData();
    formData.append('nick_name', form.nick_name);
    formData.append('email', form.email);
    formData.append('phone', form.phone);
    formData.append('age', String(form.age));
    formData.append('gender', form.gender);
    if (form.avatar) formData.append('avatar', form.avatar);  // 如果用户有上传头像，则添加到 FormData

    await updateUser(formData);  // 调用后端更新用户信息 API

    // 更新 Pinia store 中的用户数据
    loginUserStore.setLoginUser({
      ...loginUserStore.loginUser,
      ...form,
    });

    emits('update:modelValue', false);  // 关闭对话框

    ElMessage({
      message: '用户信息更新成功',
      type: 'success',
    })

  } catch (error) {
    ElNotification({
      title: 'Warning',
      message: '服务器匆忙，请稍后再试',
      type: 'warning',
    })
  }
};


const handleClose = () => {
  //点击取消恢复表单数据为最新的用户数据
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

/* 使用 :deep() 来覆盖 el-input 的边框 */
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