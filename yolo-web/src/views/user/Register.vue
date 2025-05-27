<template>
  <div id="mr-mainbody" class="container mr-mainbody">
    <div class="row">
      <div id="mr-content" class="mr-content col-xs-12">
        <div class="login-wrap"
             style="margin-bottom: 60px; margin-top: 50px">
          <div style="max-width: 540px; margin: 0 auto;">
            <a href="index.html" title="点击返回首页">
            </a>
          </div>
          <div class="login">
            <div class="page-header">
              <h1 class="login_h1">用户注册</h1>
            </div>

            <div v-if="errorMessage" style="color:red;text-align:center;font-size:16px">
              {{ errorMessage }}
            </div>

            <!-- 注册表单 -->
            <form  @submit.prevent="handleSubmit"  class="form-horizontal">

              <fieldset>
                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="account" class="required">账号：</label>

                  </div>
                  <div class="col-sm-8">
                    <!-- 账号文本框 -->
                    <input v-model="form.account" id="account" type="text" class="form-control" placeholder="请输入账号" required />
                    <span v-if="errors.account" class="error">{{ errors.account }}</span>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="password" class="required">密码：</label>

                  </div>
                  <div class="col-sm-8">
                    <!-- 密码文本框 -->
                    <input v-model="form.password" id="password" type="password" class="form-control" placeholder="请输入密码" required />
                    <span v-if="errors.password" class="error">{{ errors.password }}</span>

                  </div>
                </div>

                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="password" class="required">确认密码：</label>

                  </div>
                  <div class="col-sm-8">
                    <!-- 确认密码文本框 -->
                    <input v-model="form.checkPassword" id="password" type="password" class="form-control" placeholder="请确认密码" required />
                    <span v-if="errors.checkPassword" class="error">{{ errors.checkPassword }}</span>

                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="password" class="required">手机号：</label>

                  </div>
                  <div class="col-sm-8" style="clear: none;">
                    <!-- 输入联系电话的文本框 -->
                    <input v-model="form.phone" id="checkPassword" type="text" class="form-control" placeholder="请输入手机号" required />
                    <span v-if="errors.phone" class="error">{{ errors.phone }}</span>

                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="password" class="required">邮箱：</label>

                  </div>
                  <div class="col-sm-8" style="clear: none;">
                    <!-- 输入邮箱的文本框 -->
                    <input v-model="form.email" id="password" type="text" class="form-control" placeholder="请输入邮箱" required />
                    <span v-if="errors.email" class="error">{{ errors.email }}</span>


                  </div>
                </div>

                <div class="form-group">
                  <div class="col-sm-offset-4 col-sm-8">
                    <button type="submit" class="btn btn-primary login">注册</button>
                  </div>
                </div>
                <div class="form-group" style="border-top: 1px solid #D9D9D9; margin: 20px;">
                  <label style="float: right; color: #858585; margin-right: 80px; margin-top: 10px; font-size: 14px;">
                    已有账号！<router-link to="/login">立即登录</router-link></label>
                </div>
              </fieldset>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">

import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { register } from "@/api/login/user";
const errorMessage = ref('');

const form = ref({
  account:'',
  // nick_name: '',
  password: '',
  checkPassword: '',
  phone:'',
  email:'',

});

const errors = ref<any>({}); // 用于存储表单验证错误
const loading = ref(false);
const router = useRouter();

// 正则表达式：账号只能包含字母、数字和下划线，且不允许有中文字符
const accountRegExp = /^[a-zA-Z0-9_]+$/;

// 表单提交处理
const handleSubmit = async () => {
  // 清除之前的错误信息
  errors.value = {};

  // 验证账号格式
  if (!accountRegExp.test(form.value.account)) {
    errors.value.account = '账号只能包含字母、数字和下划线，且不能包含中文字符';
    return;
  }
  // 验证密码和确认密码是否一致
  if (form.value.password !== form.value.checkPassword) {
    errors.value.checkPassword = '密码和确认密码不一致';
    return;
  }

  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await register(form.value);

    if (response.data.success) {
      router.push('/login');
    } else {
      errors.value = response.data.errors || {}; // 获取后端返回的错误
    }
  } catch (error) {
    console.error('Register failed:', error);
    errorMessage.value = '注册失败，请稍后再试';
  } finally {
    loading.value = false;
  }
};


</script>


<style scoped>
/* 样式设置 */
.login-wrap {
  max-width: 540px;
  margin: 0 auto;
  padding: 20px;
  background: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.page-header {
  text-align: center;
}

.login_h1 {
  font-size: 28px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-control {
  width: 80%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
}


.error {
  color: red;
  font-size: 12px;
}

.btn-primary:disabled {
  background-color: #e0e0e0;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>