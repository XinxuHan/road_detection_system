<!--<template>-->

<!--  <div>-->
<!--    <el-card>-->
<!--      <el-descriptions class="margin-top" title="重置密码" :column="2" border>-->

<!--      </el-descriptions>-->

<!--      <el-row class="password-change">-->
<!--        <el-col :span="14">-->
<!--          <el-form-->
<!--              :model="pwdForm"-->
<!--              :rules="rules"-->
<!--              ref="formRef"-->
<!--              label-width="100px"-->
<!--              size="large"-->

<!--          >-->
<!--            <el-form-item label="原密码" prop="old_pwd">-->
<!--              <el-input v-model="pwdForm.old_pwd" type="password"></el-input>-->

<!--            </el-form-item>-->
<!--            <el-form-item label="新密码" prop="new_pwd">-->
<!--              <el-input v-model="pwdForm.new_pwd" type="password"></el-input>-->
<!--            </el-form-item>-->
<!--            <el-form-item label="确认新密码" prop="re_pwd">-->
<!--              <el-input v-model="pwdForm.re_pwd" type="password"></el-input>-->
<!--            </el-form-item>-->
<!--            <el-form-item>-->
<!--              <el-button @click="onSubmit" type="primary">确定修改</el-button>-->
<!--              <el-button @click="onReset((formRef))">清除</el-button>-->
<!--            </el-form-item>-->
<!--          </el-form>-->
<!--        </el-col>-->
<!--      </el-row>-->


<!--    </el-card>-->


<!--  </div>-->

<!--</template>-->


<!--<script setup lang="ts" >-->
<!--import { ref } from 'vue'-->
<!--import {ElMessage, type FormInstance, type FormRules} from 'element-plus'-->
<!--import {updatePassword} from "@/api/login/user";-->
<!--import {useLoginUserStore} from "@/store/useLoginUserStore";-->
<!--import router from "@/router";-->
<!--const formRef = ref<FormInstance>()-->
<!--const loginUserStore = useLoginUserStore();-->

<!--const pwdForm = ref({-->
<!--  old_pwd: '',-->
<!--  new_pwd: '',-->
<!--  re_pwd: ''-->
<!--})-->

<!--const checkOldSame = (rule:any, value:any, callback: any) => {-->
<!--  if (value === pwdForm.value.old_pwd) {-->
<!--    callback(new Error('原密码和新密码不能一样!'))-->
<!--  } else {-->
<!--    callback()-->
<!--  }-->
<!--}-->

<!--const checkNewSame = (rule:any, value:any, callback: any) => {-->
<!--  if (value !== pwdForm.value.new_pwd) {-->
<!--    callback(new Error('新密码和确认再次输入的新密码不一样!'))-->
<!--  } else {-->
<!--    callback()-->
<!--  }-->
<!--}-->
<!--const rules = {-->
<!--  // 原密码-->
<!--  old_pwd: [-->
<!--    { required: true, message: '请输入密码', trigger: 'blur' },-->
<!--    {-->
<!--      pattern: /^\S{6,15}$/,-->
<!--      message: '密码长度必须是6-15位的非空字符串',-->
<!--      trigger: 'blur'-->
<!--    }-->
<!--  ],-->
<!--  // 新密码-->
<!--  new_pwd: [-->
<!--    { required: true, message: '请输入新密码', trigger: 'blur' },-->
<!--    {-->
<!--      pattern: /^\S{6,15}$/,-->
<!--      message: '密码长度必须是6-15位的非空字符串',-->
<!--      trigger: 'blur'-->
<!--    },-->
<!--    { validator: checkOldSame, trigger: 'blur' }-->
<!--  ],-->
<!--  // 确认新密码-->
<!--  re_pwd: [-->
<!--    { required: true, message: '请再次确认新密码', trigger: 'blur' },-->
<!--    {-->
<!--      pattern: /^\S{6,15}$/,-->
<!--      message: '密码长度必须是6-15位的非空字符串',-->
<!--      trigger: 'blur'-->
<!--    },-->
<!--    { validator: checkNewSame, trigger: 'blur' }-->
<!--  ]-->
<!--}-->


<!--// 提交表单，修改密码-->
<!--const onSubmit = async () => {-->
<!--  // 校验表单-->
<!--  const isValid = await formRef.value?.validate();-->
<!--  if (!isValid) return;-->

<!--  const { old_pwd, new_pwd } = pwdForm.value;-->

<!--  try {-->
<!--    const response = await updatePassword({-->
<!--      old_password: old_pwd,-->
<!--      new_password: new_pwd,-->
<!--      email: loginUserStore.loginUser.email-->
<!--    });-->

<!--    if(response.data.code == 200){-->
<!--      // 修改密码成功后，清空本地存储的用户信息-->
<!--      loginUserStore.clearLoginUser();-->
<!--      // 跳转到登录页面-->
<!--      router.push({ name: 'login' });-->
<!--      ElMessage({-->
<!--        message: '密码修改成功,请重新登录！',-->
<!--        type: 'success',-->
<!--      })-->
<!--    } else {-->
<!--      ElMessage.error(response.data.error)-->
<!--    }-->
<!--  } catch (error) {-->
<!--    console.error('修改密码失败:', error);-->
<!--  }-->
<!--};-->



<!--const onReset = (formEl: FormInstance | undefined) => {-->
<!--  if (!formEl) return-->
<!--  formEl.resetFields()-->
<!--}-->


<!--</script>-->




<!--<style scoped>-->

<!--/* 使用 :deep() 来覆盖 el-input 的边框 */-->
<!--:deep(.el-input__wrapper) {-->
<!--  padding: 0 !important;-->
<!--}-->
<!--/* 让 el-row 包裹的内容看起来像方框 */-->
<!--.password-change {-->

<!--  justify-content: center; /* 水平居中 */-->
<!--  align-items: center; /* 垂直居中 */-->
<!--}-->




<!--</style>-->