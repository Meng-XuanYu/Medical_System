import { defineStore } from 'pinia';
import http from './http';
import { Response } from '@/types';
import { useMenuStore } from './menu';
import { useAuthStore } from '@/plugins';
import { useLoadingStore } from './loading';
import { ElMessage } from 'element-plus';
import 'element-plus/dist/index.css';
import router from "@/router";

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
}

export type TokenResult = {
  token: string;
  expires: number;
};
export const useAccountStore = defineStore('account', {
  state() {
    return {
      account: {} as Account,
      permissions: [] as string[],
      role: '',
      logged: true,
      userType: '',
    };
  },
  actions: {
    logged: undefined,
    async Register( account: AccountParams
      ) {
      fetch('/api/user/register', {
        method: 'POST',
        body: JSON.stringify({
          id: account.username,
          password: account.password,
          name: account.name,
          gender: account.gender,
          birth: account.borndate,
          id_number: account.identity,
          usertype: account.usertype,
          phone: account.phone,

        })
      })
          .then(response => response.json())
          .then(data => {
            if (data.status === 'success') {
              ElMessage.success('注册成功, 自动跳转到登录页面');
              setTimeout(null, 1000);
              router.push('/login');
            } else {
              ElMessage.error('注册失败：' + data.message);
              console.error('注册失败:'+ data.message);
            }
          })
    },
    async login(username: string, password: string, userType: string) {
      const id = username;
      return http
          .request<TokenResult,Response<any>>('/login', 'post_json', { id, password, userType })
          .then(async (response) => {
            if (response.data.status === 'success') {
              this.logged = true;
              http.setAuthorization(`Bearer ${response.data.token}`, new Date(response.data.expires));

              await useMenuStore().getMenuList(userType);

              this.userType = userType;
              switch (userType) {
                case 'a':
                  await router.push('/admin_doctor');
                  break;
                case 't':
                  await router.push('/workplace');
                  break;
                case 's':
                  await router.push('/workplace');
                  break;
                default:
                  await router.push('/myarrange');
              }
              return response.data;
            } else {
              return Promise.reject(response.message);
            }
          });
    },
    async logout() {

      return new Promise<boolean>((resolve) => {
        localStorage.removeItem('stepin-menu');
        http.removeAuthorization();
        this.logged = false;
        router.replace('/home');
        resolve(true);

      });
    },
    async profile() {
      const { setAuthLoading } = useLoadingStore();
      setAuthLoading(true);
      return http
        .request<Account, Response<Profile>>('/account', 'get')
        .then((response) => {
          if (response.code === 0) {
            const { setAuthorities } = useAuthStore();
            const { account, permissions, role } = response.data;
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
});
