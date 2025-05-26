import { createRouter, createWebHistory } from 'vue-router';
import Detect from "@/views/Detect.vue";
import Login from "@/views/user/Login.vue";
import Register from "@/views/user/Register.vue";
import UserCenter from "@/views/user/UserCenter.vue";
import HelloWorld from "@/components/HelloWorld.vue";
import {useLoginUserStore} from "@/store/useLoginUserStore";

const routes = [
    {
        path: '/',
        redirect: '/hello'  // 当访问根路径时，重定向到 /hello
    },

    {
        path: '/detect',
        name: 'Detect',
        component: Detect, // 实际的组件
        meta: { requiresAuth: true }, // 需要登录
    },
    {
        path: '/hello',
        name: 'HelloWorld',
        component: HelloWorld // 实际的组件
    },
    {
        path: '/login',
        name: 'login',
        component: Login // 实际的组件
    },
    {
        path: '/register',
        name: 'register',
        component: Register // 实际的组件
    },
    {
        path: '/user/center',
        name: 'UserCenter',
        component: UserCenter,
        meta: { requiresAuth: true }, // 需要登录
        redirect: '/user/center/info/:id',
        children: [
            {
                path: '/user/center/info/:id',
                name:'info',
                component: () => import('@/views/user/Info.vue')

            },

            {
                path: '/user/center/ChangePassword/:id',
                name:'ChangePassword',
                component: () => import('@/views/user/ChangePassword.vue')

            },
        ]
    },

    

];

const router = createRouter({
    history: createWebHistory(),
    routes
});


router.beforeEach((to, from, next) => {
    const loginUserStore = useLoginUserStore();
    const requiresAuth = to.meta.requiresAuth;

    if (requiresAuth && !loginUserStore.isLoggedIn) {
        next({
            path: '/login',
            query: { redirect: to.fullPath }
        });
    } else {
        next();
    }
});

export default router;
