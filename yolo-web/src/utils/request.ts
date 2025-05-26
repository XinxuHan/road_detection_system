import axios from 'axios';
import {ElMessage, ElNotification} from "element-plus";

const myApi = axios.create({
    baseURL: 'http://localhost:8000',  // 你的 Django 后端地址
    timeout: 10000,  // 设置请求超时时间
    headers: { 'Content-Type': 'application/json;charset=UTF-8' },  // 请求头
    withCredentials: true  // 确保请求携带 Cookie（包括 sessionid）
});



// 添加请求拦截器
axios.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    return config;
}, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
});


// 响应拦截器（处理响应状态码，错误处理）
myApi.interceptors.response.use(
    (response) => {
        console.log(response); // 打印响应值
        const { data } = response;
        console.log(data);
        if (data.code === 401) {
            ElNotification({
                title: "你还没有登录哟~",
                message: response.data.msg,
                type: "error",
                }
            )

        }
        if (data.code === 500) {
            ElNotification({
                title: "服务器内部错误",
                message: response.data.msg,
                type: "error",
            });
        }
        return response;
    },
);


export default myApi;
