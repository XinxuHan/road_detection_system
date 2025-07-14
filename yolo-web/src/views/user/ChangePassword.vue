<template>
  <div>
    <el-card>
      <el-descriptions
        class="margin-top"
        title="Reset Password"
        :column="2"
        border
      />
      <el-row class="password-change" justify="center">
        <el-col :span="24">
          <el-form
            ref="formRef"
            :model="pwdForm"
            :rules="rules"
            label-width="200px"
            label-position="left"
            size="large"
          >
            <el-form-item label="Current Password" prop="old_pwd">
              <el-input
                type="password"
                v-model="pwdForm.old_pwd"
                :style="{ width: '400px' }"
              />
            </el-form-item>

            <el-form-item label="New Password" prop="new_pwd">
              <el-input
                type="password"
                v-model="pwdForm.new_pwd"
                :style="{ width: '400px' }"
              />
            </el-form-item>

            <el-form-item label="Confirm New Password" prop="re_pwd">
              <el-input
                type="password"
                v-model="pwdForm.re_pwd"
                :style="{ width: '400px' }"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="onSubmit">
                Update Password
              </el-button>
              <el-button @click="() => onReset(formRef)">
                Reset
              </el-button>
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

const checkOldSame = (rule:any, value:any, callback: Function) => {
  if (value === pwdForm.value.old_pwd) {
    callback(new Error('New password cannot be the same as the current password!'))
  } else {
    callback()
  }
}

const checkNewSame = (rule:any, value:any, callback: Function) => {
  if (value !== pwdForm.value.new_pwd) {
    callback(new Error('Confirmation password does not match the new password!'))
  } else {
    callback()
  }
}
const rules: FormRules = {
  old_pwd: [
    {
      required: true,
      message: 'Please input your current password',
      trigger: 'blur'
    },
    {
      pattern: /^\S{6,15}$/,
      message: 'Password must be 6–15 non-whitespace characters.',
      trigger: 'blur'
    }
  ],
  new_pwd: [
    {
      required: true,
      message: 'Please input your new password',
      trigger: 'blur'
    },
    {
      pattern: /^\S{6,15}$/,
      message: 'Password must be 6–15 non-whitespace characters.',
      trigger: 'blur'
    },
    {
      validator: checkOldSame,
      trigger: 'blur'
    }
  ],
  re_pwd: [
    {
      required: true,
      message: 'Please confirm your new password',
      trigger: 'blur'
    },
    {
      pattern: /^\S{6,15}$/,
      message: 'Password must be 6–15 non-whitespace characters.',
      trigger: 'blur'
    },
    {
      validator: checkNewSame,
      trigger: 'blur'
    }
  ]
}


// Submit the form to change the password
const onSubmit = async () => {
  // Validation form
  const valid = await formRef.value?.validate()
  if (!valid) return

  const { old_pwd, new_pwd } = pwdForm.value;

  try {
    const response = await updatePassword({
      old_password: old_pwd,
      new_password: new_pwd,
      email: loginUserStore.loginUser.email
    });

    const code = response.data.code
    const error = response.data.error

    if(code == 200){
      // After the password is successfully changed, clear the locally stored user information
      loginUserStore.clearLoginUser();
      // Jump to the login page
      router.push('/login');
      ElMessage({
        message: 'Password modification successful, please log in again!',
        type: 'success',
      })
    } else {
      ElMessage.error(error)
    }
  } catch (err) {
    console.error('Password change failed:', err);
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