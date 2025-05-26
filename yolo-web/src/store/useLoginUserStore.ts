import { defineStore } from "pinia";
import {computed, ref} from "vue";

// 定义用户信息
interface User {
    nick_name: string;
    account: string;
    avatar: string;
    email: string;
    phone: string;
    gender: string;
    age: number;
    addtime: string;

}


export const useLoginUserStore = defineStore('LoginUserStore', () => {
    // const loginUser = ref<User | null>(null);  // 默认为 null，表示未登录
    const loginUser = ref();  // 默认为 null，表示未登录

    // 刷新页面的话用户依然存在
    if (localStorage.getItem('user')) {
        loginUser.value = JSON.parse(localStorage.getItem('user')!);
    }

    // 判断是否登录的 getter
    const isLoggedIn = computed(() => !!loginUser.value);

    // 设置用户信息
    function setLoginUser(user: User) {
        loginUser.value = user;
        localStorage.setItem('user', JSON.stringify(user)); // 更新到本地存储
    }

    // 退出账号
    function clearLoginUser() {
        loginUser.value = null;
        localStorage.removeItem('user');  // 清除本地存储中的用户信息
    }

    return { loginUser,isLoggedIn, setLoginUser, clearLoginUser };
});
