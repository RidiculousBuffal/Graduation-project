import type {userType} from "../store/user/types.ts";
import { updateUserInfo} from "../api/userapi.ts";
import {useUserStore} from "../store/user/userStore.ts";

export class UserService {
    public static async updateUserInfo(user: Partial<userType>) {
        const current_user_info = useUserStore.getState().user
        const u = await updateUserInfo({
            ...user,
            faceInfo: current_user_info.faceInfo,
        })
        if (u) {
            //     成功更新
            useUserStore.getState().setUser(u)
            return true
        } else {
            return false
        }
    }


}