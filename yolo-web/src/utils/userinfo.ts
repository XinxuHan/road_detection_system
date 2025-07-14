    // src/utils/user.ts

    import { useLoginUserStore } from "@/store/useLoginUserStore";
    import { reactive, watchEffect } from "vue";
    import myApi from "@/utils/request";

    const defaultAvatarUrl = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png';

    // Define responsive states for user avatar and username
    const state = reactive({
        avatarUrl: defaultAvatarUrl,  

    });

    // Get username and avatar information
    export function useUserInfo() {
        const loginUserStore = useLoginUserStore();

        // Monitor changes in user information
        watchEffect(() => {
            const userAvatarPath = loginUserStore.loginUser?.avatar;  
            state.avatarUrl = userAvatarPath ? `${myApi.defaults.baseURL}${userAvatarPath}` : defaultAvatarUrl;  
        });

        return state;  
    }
