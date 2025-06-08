import {login, register} from '../api/userapi';
import {useUserStore} from '../store/user/userStore';
import message from '../components/globalMessage';
import {initUserInfoState} from "../store/user/initState.ts";

export class AuthService {
    /**
     * 用户登录
     * @param username 用户名
     * @param password 密码
     * @returns 登录是否成功
     */
    static async login(username: string, password: string): Promise<boolean> {
        try {
            const response = await login(username, password);
            if (response) {
                // 将登录信息存储到 zustand 中
                useUserStore.getState().setAccessToken(response.access_token);
                useUserStore.getState().setRefreshToken(response.refresh_token);
                useUserStore.getState().setUser(response.payload.user);
                useUserStore.getState().setPermissions(response.payload.permissions);
                useUserStore.getState().setRoles(response.payload.role);
                message.success('登录成功');
                return true;
            }
            return false;
        } catch (error) {
            message.error('登录失败');
            return false;
        }
    }

    /**
     * 用户注册
     * @param username 用户名
     * @param password 密码
     * @param email 邮箱
     * @returns 注册是否成功
     */
    static async register(username: string, password: string, email: string): Promise<boolean> {
        try {
            const response = await register(username, password, email);
            message.success('注册成功');
            return true;

        } catch (error) {
            message.error('注册失败');
            return false;
        }
    }

    /**
     * 退出登录
     */
    static logout(): void {
        useUserStore.getState().setAccessToken(null);
        useUserStore.getState().setRefreshToken(null);
        useUserStore.getState().setUser(initUserInfoState);
        useUserStore.getState().setPermissions([]);
        useUserStore.getState().setRoles([]);
        message.success('已退出登录');
    }

    /**
     * 检查用户是否已登录
     * @returns 是否已登录
     */
    static isLoggedIn(): boolean {
        const {access_token} = useUserStore.getState();
        return access_token !== null;
    }
}
