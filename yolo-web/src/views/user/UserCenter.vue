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
            >编辑</el-button>

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
              <span slot="title">个人简介</span>
            </el-menu-item>

            <el-menu-item
                index="ChangePassword"
                :route="{ name: 'ChangePassword', params: { id: loginUserStore.loginUser?.id } }">

              <i class="el-icon-edit-outline"></i>
              <span slot="title">修改密码</span>
            </el-menu-item>



          </el-menu>


        </el-card>
      </div>
      <div class="person_body_right">

        <router-view></router-view>
      </div>
    </div>
    <!-- 引入 PersonalDia 组件 -->
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

// 通过 computed 获取用户数据并更新 UI
computed(() => loginUserStore.loginUser);

// 控制对话框的显示与隐藏
const dialogVisible = ref(false);


const openEditDialog = () => {
  dialogVisible.value = true;  // 设置对话框可见
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
  padding: 20px; /* 添加内边距，使其看起来像卡片 */
  background-color: white;
  margin-top: 30px;
  position: relative;  /* 为了与绝对定位的元素对齐 */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  -webkit-box-shadow: 0 4px 8px 6px rgba(7, 17, 27, .06);
  box-shadow: 0 4px 8px 6px rgba(7, 17, 27, .06);
  overflow: hidden; /* 防止内容溢出 */
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
  background-color: #ecf5ff; /* 激活项的背景颜色 */
}

.el-menu-item.is-active > span {
  color: #00c3ff; /* 激活时字体颜色 */
}

/*下面部分样式*/
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
      90deg,  /* 使用标准角度值 */
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

