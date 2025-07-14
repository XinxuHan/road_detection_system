import axios from 'axios';
import {ElMessage, ElNotification} from "element-plus";

const myApi = axios.create({
    baseURL: 'http://localhost:8000',  // Your Django backend address
    timeout: 10000,  // Set request timeout
    headers: { 'Content-Type': 'application/json;charset=UTF-8' },  // Request Header
    withCredentials: true  // Make sure the request carries cookies (including sessionid)
});



// Add a request interceptor
axios.interceptors.request.use(function (config) {
    return config;
}, function (error) {
    return Promise.reject(error);
});


// Response interceptor (processing response status code, error handling)
myApi.interceptors.response.use(
    (response) => {
        console.log(response); // Print the response value
        const { data } = response;
        console.log(data);
        if (data.code === 401) {
            ElNotification({
                title: "You haven't logged in yet",
                message: response.data.msg,
                type: "error",
                }
            )

        }
        if (data.code === 500) {
            ElNotification({
                title: "Internal server error",
                message: response.data.msg,
                type: "error",
            });
        }
        return response;
    },
);


export default myApi;
