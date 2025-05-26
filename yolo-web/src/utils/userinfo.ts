    // src/utils/user.ts

    import { useLoginUserStore } from "@/store/useLoginUserStore";
    import { reactive, watchEffect } from "vue";
    import myApi from "@/utils/request";

    // 默认头像 URL
    const defaultAvatarUrl = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';

    // 定义用户头像和用户名的响应式状态
    const state = reactive({
        avatarUrl: defaultAvatarUrl,  // 默认头像

    });

    // 获取用户名和头像信息
    export function useUserInfo() {
        const loginUserStore = useLoginUserStore();

        // 监控用户信息的变化
        watchEffect(() => {
            const userAvatarPath = loginUserStore.loginUser?.avatar;  // 获取用户头像的相对路径
            state.avatarUrl = userAvatarPath ? `${myApi.defaults.baseURL}${userAvatarPath}` : defaultAvatarUrl;  // 拼接头像 URL
        });

        return state;  // 返回响应式的头像 URL 和用户名
    }
