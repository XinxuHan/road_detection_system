<template>
  <div id="mr-mainbody" class="container mr-mainbody">
    <div class="row">
      <div id="mr-content" class="mr-content col-xs-12">
        <div class="login-wrap" style="margin-bottom: 60px; margin-top: 50px;">
          <div style="max-width: 540px; margin: 0 auto;">
<!--            <a href="/" title="Click to return to the home page">-->
<!--              <img src="../assets/logo.svg" alt="Back to Home" />-->
<!--            </a>-->
          </div>
          <div class="login">
            <div class="page-header">
              <h1 class="login_h1">User login</h1>
            </div>

            <!-- error message -->
            <div v-if="errorMessage" style="color:red;text-align:center;font-size:16px">
              {{ errorMessage }}
            </div>

            <form @submit.prevent="handleSubmit" class="form-horizontal">
              <div class="form-group">
                <div class="col-sm-4 control-label">
                  <label for="account" class="required">account:</label>
                </div>
                <div class="col-sm-8">
                  <input v-model="form.account" id="account" type="text" class="form-control" placeholder="Please enter your account number" required />
                </div>
              </div>
              <div class="form-group">
                <div class="col-sm-4 control-label">
                  <label for="password" class="required">password:</label>
                </div>
                <div class="col-sm-8">
                  <input v-model="form.password" id="password" type="password" class="form-control" placeholder="Please enter your password" required />
                </div>
              </div>

              <div class="form-group">
                <div class="col-sm-offset-4 col-sm-8">
                  <button type="submit" class="btn btn-primary login" :disabled="loading">
                    Login
                  </button>
                </div>
              </div>

              <div class="form-group" style="border-top: 1px solid #D9D9D9; margin: 20px;">
                <label style="float: right; color: #858585; margin-right: 40px; margin-top: 10px; font-size: 14px;">
                  No account?<router-link to="/register">Register Now</router-link>
                </label>
              </div>
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
import { login } from "@/api/login/user";
import {useLoginUserStore} from "@/store/useLoginUserStore";
import {carouselContextKey} from "element-plus";


// Define form data and loading status
const form = ref({
  account: '',
  password: ''
});

const loading = ref(false);
const errorMessage = ref('');

const router = useRouter();
const loginUserStore  = useLoginUserStore();



const handleSubmit = async () => {
  loading.value = true;
  errorMessage.value = ''; // Clear previous error messages

  try {
    // Login request, make sure username and password are passed
    const response = await login({
      account: form.value.account,
      password: form.value.password
    });

    // Login successful, process user information
    if (response.data.success) {
      loginUserStore.setLoginUser(response.data.user);
      //console.log(response.data.user);
      // Login successful, save user information to localStorage
      localStorage.setItem('user', JSON.stringify(response.data.user));
      router.push('/');
    } else {
      // The backend returns an error message
      errorMessage.value = response.data.error
    }
  } catch (error) {
    console.error('Login failed:', error);
    // Error message when processing fails
    errorMessage.value = 'The system is busy, please try again later!';
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
