<template>
  <div id="mr-mainbody" class="container mr-mainbody">
    <div class="row">
      <div id="mr-content" class="mr-content col-xs-12">
        <div class="login-wrap"
             style="margin-bottom: 60px; margin-top: 50px">
          <div style="max-width: 540px; margin: 0 auto;">
            <a href="index.html" title="Click to return to the home page">
            </a>
          </div>
          <div class="login">
            <div class="page-header">
              <h1 class="login_h1">User Registration</h1>
            </div>

            <div v-if="errorMessage" style="color:red;text-align:center;font-size:16px">
              {{ errorMessage }}
            </div>

            <!-- Registration form -->
            <form  @submit.prevent="handleSubmit"  class="form-horizontal">

              <fieldset>
                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="account" class="required">账号：</label>

                  </div>
                  <div class="col-sm-8">
                    <!-- Account text box -->
                    <input v-model="form.account" id="account" type="text" class="form-control" placeholder="Please enter your account number" required />
                    <span v-if="errors.account" class="error">{{ errors.account }}</span>
                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="password" class="required">密码：</label>

                  </div>
                  <div class="col-sm-8">
                    <!-- Password text box -->
                    <input v-model="form.password" id="password" type="password" class="form-control" placeholder="Please enter your password" required />
                    <span v-if="errors.password" class="error">{{ errors.password }}</span>

                  </div>
                </div>

                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="password" class="required">确认密码：</label>

                  </div>
                  <div class="col-sm-8">
                    <!-- Confirm Password Text Box -->
                    <input v-model="form.checkPassword" id="password" type="password" class="form-control" placeholder="Please confirm your password" required />
                    <span v-if="errors.checkPassword" class="error">{{ errors.checkPassword }}</span>

                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="password" class="required">手机号：</label>

                  </div>
                  <div class="col-sm-8" style="clear: none;">
                    <!-- Text box for entering contact phone number -->
                    <input v-model="form.phone" id="checkPassword" type="text" class="form-control" placeholder="Please enter your phone number" required />
                    <span v-if="errors.phone" class="error">{{ errors.phone }}</span>

                  </div>
                </div>
                <div class="form-group">
                  <div class="col-sm-4 control-label">
                    <label for="password" class="required">Email:</label>

                  </div>
                  <div class="col-sm-8" style="clear: none;">
                    <!-- Text box for entering email address -->
                    <input v-model="form.email" id="password" type="text" class="form-control" placeholder="Please enter your email address" required />
                    <span v-if="errors.email" class="error">{{ errors.email }}</span>


                  </div>
                </div>

                <div class="form-group">
                  <div class="col-sm-offset-4 col-sm-8">
                    <button type="submit" class="btn btn-primary login">register</button>
                  </div>
                </div>
                <div class="form-group" style="border-top: 1px solid #D9D9D9; margin: 20px;">
                  <label style="float: right; color: #858585; margin-right: 80px; margin-top: 10px; font-size: 14px;">
                    Already have an account!<router-link to="/login">Sign in now</router-link></label>
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

const errors = ref<any>({}); // Used to store form validation errors
const loading = ref(false);
const router = useRouter();

// Regular expression: The account number can only contain letters, numbers, and underscores, and Chinese characters are not allowed.
const accountRegExp = /^[a-zA-Z0-9_]+$/;

// Form submission processing
const handleSubmit = async () => {
  // Clear previous error messages
  errors.value = {};

  // Verify account format
  if (!accountRegExp.test(form.value.account)) {
    errors.value.account = 'The account number can only contain letters, numbers and underscores, and cannot contain Chinese characters';
    return;
  }
  // Verify that the password and confirm password are the same
  if (form.value.password !== form.value.checkPassword) {
    errors.value.checkPassword = 'The password and confirm password do not match';
    return;
  }

  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await register(form.value);

    if (response.data.success) {
      router.push('/login');
    } else {
      errors.value = response.data.errors || {}; // Get the error returned by the backend
    }
  } catch (error) {
    console.error('Register failed:', error);
    errorMessage.value = 'Registration failed, please try again later';
  } finally {
    loading.value = false;
  }
};


</script>


<style scoped>
/* Style Settings */
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