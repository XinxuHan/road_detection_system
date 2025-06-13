import { defineStore } from "pinia";
import {computed, ref} from "vue";

// Define user information
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
    // const loginUser = ref<User | null>(null);  // The default value is null, indicating that the user is not logged in.
    const loginUser = ref();  // The default value is null, indicating that the user is not logged in.

    // If you refresh the page, the user still exists
    if (localStorage.getItem('user')) {
        loginUser.value = JSON.parse(localStorage.getItem('user')!);
    }

    // Getter to determine whether to log in
    const isLoggedIn = computed(() => !!loginUser.value);

    // Set user information
    function setLoginUser(user: User) {
        loginUser.value = user;
        localStorage.setItem('user', JSON.stringify(user)); // Update to local storage
    }

    // Log out
    function clearLoginUser() {
        loginUser.value = null;
        localStorage.removeItem('user');  // Clear user information in local storage
    }

    return { loginUser,isLoggedIn, setLoginUser, clearLoginUser };
});
