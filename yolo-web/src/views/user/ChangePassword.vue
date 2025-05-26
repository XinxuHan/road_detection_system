<template>

  <div>
    <el-card>
      <el-descriptions class="margin-top" title="Reset Password" :column="2" border>

      </el-descriptions>

      <el-row class="password-change">
        <el-col :span="14">
          <el-form
              :model="pwdForm"
              :rules="rules"
              ref="formRef"
              label-width="100px"
              size="large"

          >
            <el-form-item label="Current Password" prop="old_pwd">
              <el-input v-model="pwdForm.old_pwd" type="password"></el-input>

            </el-form-item>
            <el-form-item label="New Password" prop="new_pwd">
              <el-input v-model="pwdForm.new_pwd" type="password"></el-input>
            </el-form-item>
            <el-form-item label="Confirm New Password" prop="re_pwd">
              <el-input v-model="pwdForm.re_pwd" type="password"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="onSubmit" type="primary">Confirm the changes</el-button>
              <el-button @click="onReset((formRef))">Clear</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>


    </el-card>


  </div>

</template>


<script setup lang="ts" >
import { ref } from 'vue'
import {ElMessage, type FormInstance, type FormRules} from 'element-plus'
import {updatePassword} from "@/api/login/user";
import {useLoginUserStore} from "@/store/useLoginUserStore";
import router from "@/router";
const formRef = ref<FormInstance>()
const loginUserStore = useLoginUserStore();

const pwdForm = ref({
  old_pwd: '',
  new_pwd: '',
  re_pwd: ''
})

const checkOldSame = (rule:any, value:any, callback: any) => {
  if (value === pwdForm.value.old_pwd) {
    callback(new Error('The original password and the new password cannot be the same!'))
  } else {
    callback()
  }
}

const checkNewSame = (rule:any, value:any, callback: any) => {
  if (value !== pwdForm.value.new_pwd) {
    callback(new Error('The new password and the new password you enter again to confirm are different!'))
  } else {
    callback()
  }
}
const rules = {
  // Original password
  old_pwd: [
    { required: true, message: 'Please enter your password', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: 'The password must be a non-empty string of 6-15 characters.',
      trigger: 'blur'
    }
  ],
  // New Password
  new_pwd: [
    { required: true, message: 'Please enter new password', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: 'The password must be a non-empty string of 6-15 characters.',
      trigger: 'blur'
    },
    { validator: checkOldSame, trigger: 'blur' }
  ],
  // Confirm New Password
  re_pwd: [
    { required: true, message: 'Please confirm your new password again', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: 'The password must be a non-empty string of 6-15 characters.',
      trigger: 'blur'
    },
    { validator: checkNewSame, trigger: 'blur' }
  ]
}


// Submit the form to change the password
const onSubmit = async () => {
  // Validation form
  const isValid = await formRef.value?.validate();
  if (!isValid) return;

  const { old_pwd, new_pwd } = pwdForm.value;

  try {
    const response = await updatePassword({
      old_password: old_pwd,
      new_password: new_pwd,
      email: loginUserStore.loginUser.email
    });

    if(response.data.code == 200){
      // After the password is changed successfully, clear the locally stored user information
      loginUserStore.clearLoginUser();
      // Jump to the login page
      router.push({ name: 'login' });
      ElMessage({
        message: 'Password modification successful, please log in again!',
        type: 'success',
      })
    } else {
      ElMessage.error(response.data.error)
    }
  } catch (error) {
    console.error('Password change failed:', error);
  }
};



const onReset = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}


</script>




<style scoped>

/* Use :deep() to cover the border of el-input */
:deep(.el-input__wrapper) {
  padding: 0 !important;
}
/* Make the content wrapped by el-row look like a box */
.password-change {

  justify-content: center; /* Horizontal Center */
  align-items: center; /* Vertical Center */
}




</style>