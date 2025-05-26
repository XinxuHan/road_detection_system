<template>
  <div class="header-layout">

    <div class="logo">
      <img  class="logo-img" src="../assets/logo.svg" alt="logo" />
      <div class="title">Recognition System</div>
    </div>

    <!-- Website header -->
    <header id="mr-header" class="wrap mr-header">
      <div class="container">
        <div class="row">
          <!-- Main navigation bar -->
          <nav id="mr-mainnav" class="col-xs-12 col-md-6 mr-mainnav navbar navbar-default">
            <div class="mr-navbar navbar-collapse collapse">
              <div class="mr-megamenu animate slide" data-duration="400"
                   data-responsive="true">
                <ul class="nav navbar-nav level0">
                  <li itemprop="name" >
                    <RouterLink to="/hello" active-class="router-link-active">
                      HOME
                    </RouterLink>
                  </li>
                  <li itemprop="name" >
                    <RouterLink  to="/detect"  active-class="router-link-active">
                      Recognition System
                    </RouterLink>
                  </li>
                  <li itemprop="name" >
                    <RouterLink  to="/user/center"  active-class="router-link-active">
                      My Profile
                    </RouterLink>
                  </li>


                </ul>
              </div>
            </div>
          </nav>
          <!-- //Main navigation bar -->
        </div>
      </div>
    </header>


<!--    </div>-->
    <div v-if="loginUserStore.loginUser" class="avatar-show" >
      <el-avatar  :src="avatarUrl"   class="avatar" />

      <el-dropdown>
        <span class="el-dropdown-link">
         {{ loginUserStore.loginUser.nick_name }}
          <el-icon class="el-icon--right">
            <arrow-down />
          </el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="logout" >Logout</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <div v-else class="header-right" >
      <RouterLink to="/login"  >Login</RouterLink>
      &nbsp;｜&nbsp;
      <RouterLink to="/register" >Register</RouterLink>
    </div>



  </div>
</template>

<script setup lang="ts">
import { ArrowDown } from '@element-plus/icons-vue'
import {reactive, ref, watchEffect} from 'vue'
import {RouterLink} from "vue-router";
import { useLoginUserStore } from "@/store/useLoginUserStore"; // Pinia store
import { useRouter } from "vue-router";
import Avatar from "@/components/Avatar.vue"; // Vue router
import myApi from "@/utils/request";
const loginUserStore = useLoginUserStore();
const router = useRouter();





// Get the profile picture URL
const avatarUrl = ref();

watchEffect(() => {
  avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${ loginUserStore.loginUser?.avatar}`
});



// User logout
const logout = () => {
  loginUserStore.clearLoginUser();
  router.push(
      {
        path: "/hello",
        replace: true,
      });
};



</script>

<style scoped>


.row {
  margin-left: -15px;
  margin-right: -15px;
}

.container {
  margin-right: auto;
  margin-left: auto;
  padding-left: 15px;
  padding-right: 15px
}

.mr-mainnav {
  border-left: 0;
  border-right: 0;
  border-radius: 0
}

.navbar-default .navbar-nav > li > a:hover, .navbar-default .navbar-nav > li > a:focus {
  color: #ffffff;
  background-color: #49494e;
}

/* Prevent navigation menu items from breaking onto new lines */
.navbar-nav {
  display: flex;
  flex-wrap: nowrap; /* Disable line breaks */
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}


.mr-header {
  height: 52px; /* Fixed navigation bar height */
  padding-top: 21px;   /* Set the top margin */
  padding-bottom: 20px; /* Set the bottom padding */
  background: #535b63;
  position: relative;
  border-radius: 0; /* Set the right angle side */
  flex: 1;
  box-sizing: border-box;
  align-items: center;
}

#mr-mainnav .router-link-active {
  border-bottom: 2px solid #d8c851; /* Yellow bottom line */
  color: #d8c851 !important; /* The font turns yellow when activated */
}



.header-layout{
  display: flex;
  background: #535b63;
  height: 52px; /* Uniform height */
}

/* Start of the left div style */
.logo{
  display: flex;   /* Left and right layout */
  align-items: center;  /* Vertical center */
  margin-left: 15px;
  flex: 0 0 300px; /* Fixed left width */
}

.title{
  padding: 0 10px;
  color: #ffffff;
  font-size: 15px;
}


.logo-img{
  height: 35px;
}
/* End of the left div style */




/* Right div style starts */
.header-right{
  padding: 0 40px;
  line-height: 50px;
  color: #ffffff;
  font-size: 15px;
}

.avatar-show{
  display: flex;   /* Left and right layout */
  align-items: center;  /* Vertical center */
  margin-left: -26px;
  padding: 0 27px;
}

.avatar {
  margin-right: 13px;  /* Right spacing */
}


.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}


</style>
