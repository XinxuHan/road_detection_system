import { createApp } from 'vue'
import App from './App.vue'
import router from "@/router";
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css';  //重点 样式必须要加
import { createPinia } from 'pinia';
import "@/assets/css/mr-01.css"; // 引入全局样式
// import * as ElementPlusIconsVue from '@element-plus/icons-vue'


const pinia = createPinia(); // 创建Pinia实例
const app = createApp(App);

app.use(router);
app.use(ElementPlus);    // 使用 ElementPlus
app.use(pinia);  // 使用 Pinia

// for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
//     app.component(key, component)
// }

app.mount('#app');



