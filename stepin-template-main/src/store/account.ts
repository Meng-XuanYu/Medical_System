import {defineStore} from 'pinia';
import http from './http';
import {Response} from '@/types';
import {useMenuStore} from './menu';
import {useAuthStore} from '@/plugins';
import {useLoadingStore} from './loading';
import {ElMessage} from 'element-plus';
import 'element-plus/dist/index.css';
import router from "@/router";
import {addRoutes, resetRouter} from "@/router/dynamicRoutes";
import routes from "@/router/routes";

export interface Profile {
    account: Account;
    permissions: string[];
    role: string;
}

export interface Account {
    username: string;
    avatar: string;
    name: string,
    gender: string,
    borndate: string,
    phone: string,
    identity: string,
    usertype: string,
}

export type AccountParams = {
    username: string;
    password: string;
    name: string,
    gender: string,
    borndate: string,
    phone: string,
    identity: string,
    usertype: string,
    image: File | null;
}

export function getCookie(name: string | any[]) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const useAccountStore = defineStore('account', {

    actions: {
        logged: undefined,
        async Register(account: any) {
            try {
                const response = await http.request('/register/user/', 'POST_JSON', account);
                const data = response.data;
                if (data.status === 'success') {
                    ElMessage.success('注册成功, 自动跳转到登录页面');
                    setTimeout(() => {
                        router.push('/login');
                    }, 1000);
                } else {
                    ElMessage.error('注册失败：' + data.message);
                    console.error('注册失败:' + data.message);
                }
            } catch (error) {
                ElMessage.error('注册失败：' + error.message);
                console.error('注册失败:', error);
            }
        },

        async login(username: string, password: string, userType: string) {
            fetch('/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // CSRF token
                },
                body: JSON.stringify({
                    id: username,
                    password: password,
                    user_type: userType,
                }),
                credentials: 'same-origin'
            })
                .then(response => response.json())
                .then(async data => {
                    if (data.status === 'success') {
                        this.logged = true;
                        http.setAuthorization(`Bearer ${data.token}`, new Date(data.expires));
                        localStorage.setItem('usertype', userType);
                        await useMenuStore().getMenuList(userType);
                        console.log(userType);
                        console.log(useMenuStore().menuList);
                        localStorage.setItem('username', username);
                        localStorage.setItem('logged', 'true');
                        localStorage.setItem('relation', '本人');
                        switch (userType) {
                            case 'a':
                                await router.push('/admin_doctor');
                                break;
                            case 't':
                                await router.push('/user_reserve');
                                break;
                            case 's':
                                await router.push('/user_reserve');
                                break;
                            default:
                                await router.push('/doctor_myarrange');
                        }
                        return data;
                    } else {
                        ElMessage.error('登录失败：' + data.message);
                        return Promise.reject(data.message);
                    }
                }).catch((error) => {
                ElMessage.error('登录失败：' + error);
            });
        },

        async logout() {
            return new Promise<boolean>((resolve) => {
                localStorage.removeItem('stepin-menu');
                http.removeAuthorization();
                this.logged = false;
                localStorage.clear();
                sessionStorage.clear();
                http.request('/logout/', 'post');
                router.clearRoutes();
                for (const route of routes) {
                    router.addRoute(route);
                }
                //resetRouter();
                router.replace('/home');
                resolve(true);
            });
        },
        async profile() {
            const {setAuthLoading} = useLoadingStore();
            setAuthLoading(true);
            return http
                .request<Account, Response<Profile>>('/account', 'get')
                .then((response) => {
                    if (response.code === 0) {
                        const {setAuthorities} = useAuthStore();
                        const {account, permissions, role} = response.data;
                        this.account = account;
                        this.permissions = permissions;
                        this.role = role;
                        setAuthorities(permissions);
                        return response.data;
                    } else {
                        return Promise.reject(response);
                    }
                })
                .finally(() => setAuthLoading(false));
        },
    },
    state() {

        return {
            account: {} as Account,
            permissions: [] as string[],
            role: '',
            logged: true,
            userType: '',
        };
    },
});
