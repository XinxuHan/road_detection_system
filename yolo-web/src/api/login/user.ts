import myApi from "@/utils/request";

/**
 * 用户登录
 */

export const login = async (params:any) => {
    return  await myApi.request({
        url:"/api/login/",
        method:"POST",
        data:params,
    })
};


/**
 * 用户注册
 */

export const register = async (params:any) => {
    return  await myApi.request({
        url:"/api/register/",
        method:"POST",
        data:params,
    })
};

/**
 * 更新用户信息
 */
export const updateUser = async (userData: any) => {
    return await myApi.request({
        url: "/api/update_user/",
        method: "POST",
        data: userData,
    });
};

/**
 * 修改密码
 */

export const updatePassword = async (params: any) => {
    return await myApi.request({
        url: "/api/update_password/",
        method: "POST",
        data: params,
    });
};