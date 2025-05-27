<template>
  <div>
    <div class="PersonTop"  >
      <div class="PersonTop_img">

        <img v-image-preview  :src="avatarUrl" />
      </div>
      <div class="PersonTop_text">
        <div class="user_text">
          <div class="user_name">
            <span> {{ loginUserStore.loginUser?.nick_name }} </span>
          </div>
          <div class="user-v" >

          </div>
          <div class="user_qianming">
            <span> </span>
          </div>
          <div >
            <el-button
                class="el-icon-edit"
                :icon="Edit"
                type="primary"
                size="medium"
                plain
                @click="openEditDialog"
            >Edit</el-button>

          </div>
        </div>
        <div class="user_num">
          <div style="cursor: pointer" @click="">
          </div>

        </div>
      </div>
    </div>

    <div class="person_body">
      <div class="person_body_left">
        <el-card class="box-card" :body-style="{ padding: '0px' }">


          <el-menu
              router
              default-active="info"
              active-text-color="#00c3ff"
              class="el-menu-vertical-demo">
            <el-menu-item
                index="info"
                :route="{ name: 'info', params: { id: loginUserStore.loginUser?.id } }">
              <i class="el-icon-user"></i>
              <span slot="title">Personal Profile</span>
            </el-menu-item>

            <el-menu-item
                index="ChangePassword"
                :route="{ name: 'ChangePassword', params: { id: loginUserStore.loginUser?.id } }">

              <i class="el-icon-edit-outline"></i>
              <span slot="title">Change Password</span>
            </el-menu-item>



          </el-menu>


        </el-card>
      </div>
      <div class="person_body_right">

        <router-view></router-view>
      </div>
    </div>
    <!-- Importing the PersonalDia component -->
    <PersonalDia  v-model="dialogVisible" />



  </div>
</template>

<script setup lang="ts">
import {  Edit } from '@element-plus/icons-vue'
import {useLoginUserStore} from "@/store/useLoginUserStore";
const loginUserStore = useLoginUserStore();


const avatarUrl = ref();


watchEffect(() => {
  avatarUrl.value = `${myApi.defaults.baseURL}/user/media/avatar/${ loginUserStore.loginUser?.avatar}`
});


import {ref, reactive, computed, watchEffect} from "vue";
import PersonalDia from "@/views/user/PersonalDia.vue";
import myApi from "@/utils/request";

// Get user data through computed and update UI
computed(() => loginUserStore.loginUser);

// Control the display and hiding of dialog boxes
const dialogVisible = ref(false);


const openEditDialog = () => {
  dialogVisible.value = true;  // Set dialog box to be visible
};









</script>

<style scoped>

.me-video-player {
  background-color: transparent;
  width: 100%;
  height: 100%;
  object-fit: fill;
  display: block;
  position: fixed;
  left: 0;
  z-index: 0;
  top: 0;
}

.PersonTop {
  width: 1000px;
  height: 160px;
  padding: 20px; /* Add padding to make it look like a card */
  background-color: white;
  margin-top: 30px;
  position: relative;  /* In order to align with absolutely positioned elements齐 */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  -webkit-box-shadow: 0 4px 8px 6px rgba(7, 17, 27, .06);
  box-shadow: 0 4px 8px 6px rgba(7, 17, 27, .06);
  overflow: hidden; /* Prevent content from overflowing */
  border-radius: 2px
}


.PersonTop_img {
  width: 130px;
  height: 120px;
  background-color: #8c939d;
  margin-right: 24px;
  margin-left: 20px;
  overflow: hidden;
  border-radius: 66px;
}

.PersonTop_img img {
  width: 100%;
  height: 100%;
  border-radius: 20px;
}

.PersonTop_text {
  height: 120px;
  width: 880px;
  display: flex;
}

.user_text {
  width: 60%;
  height: 100%;
  line-height: 30px;
}

.user_name {
  font-weight: bold;
}
.user-v {
  margin-bottom: -5px;
}
.user-v-img {
  width: 15px;
  height: 15px;
}
.user-v-font {
  font-size: 15px;
  color: #00c3ff;
}

.user_qianming {
  font-size: 14px;
  color: #999;
}



.num_text {
  color: #999;
}

.num_number {
  font-size: 20px;
  color: #333;
}



.el-menu-item.is-active {
  background-color: #ecf5ff; /* Background color of the active item */
}

.el-menu-item.is-active > span {
  color: #00c3ff; /* Font color when activated */
}

/*The following part style*/
.person_body {
  width: 1000px;
  margin-top: 30px;
  display: flex;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 5px;
}

.person_body_left {
  width: 27%;
  height: 600px;
  border-radius: 5px;
  margin-right: 3%;
  text-align: center;
}

.person_body_list {
  width: 100%;
  height: 50px;
  margin-top: 25px;
  font-size: 22px;
  border-bottom: 1px solid #f0f0f0;
  background-image: -webkit-linear-gradient(
      90deg,  /* Use standard angle values */
      rgb(42, 134, 141),
      #28506a 40%,
      rgba(204, 82, 176, 0.28) 100%
  );
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  -webkit-background-size: 200% 100%;
  -webkit-animation: masked-animation 4s linear infinite;
}

.el-menu-item {
  margin-top: 22px;
}

.person_body_right {
  width: 70%;
  /* height: 500px; */
  border-radius: 5px;
  background-color: white;
}

.box-card {
  height: 500px;
}

/*ui样式*/
.el-button {
  width: 84px;
}
</style>

