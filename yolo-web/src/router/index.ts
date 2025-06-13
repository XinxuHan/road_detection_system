import { createRouter, createWebHistory } from 'vue-router';
import Detect from "@/views/Detect.vue";
import Login from "@/views/user/Login.vue";
import Register from "@/views/user/Register.vue";
import UserCenter from "@/views/user/UserCenter.vue";
import HelloWorld from "@/components/HelloWorld.vue";
import About from "@/views/About.vue";
import {useLoginUserStore} from "@/store/useLoginUserStore";

const routes = [
    {
        path: '/',
        redirect: '/hello'  // When accessing the root path, redirect to /hello
    },

    {
        path: '/detect',
        name: 'Detect',
        component: Detect, // The actual components
        meta: { requiresAuth: true }, // Login required
    },
    {
        path: '/hello',
        name: 'HelloWorld',
        component: HelloWorld // The actual components
    },
    {
        path: '/login',
        name: 'login',
        component: Login // The actual components
    },
    {
        path: '/register',
        name: 'register',
        component: Register // The actual components
    },
    {
        path: '/user/center',
        name: 'UserCenter',
        component: UserCenter,
        meta: { requiresAuth: true }, // Login required
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

    {
        path: '/about',
        name: 'about',
        component: About // The actual components
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
