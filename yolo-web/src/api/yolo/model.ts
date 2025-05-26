import myApi from "@/utils/request";


export const switchModel = async (modelName: string) => {
    return await myApi.request({
        url: "/api/set_model/",
        method: "POST",
        data: { model_name: modelName },
    });
};




export const setModelParams = async (confidence: number, iou: number) => {
    return await myApi.request({
        url: "/api/set_model_params/",
        method: "POST",
        data: { confidence, iou },
    });
};