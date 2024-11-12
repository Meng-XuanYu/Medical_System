// store/menu.ts
import { defineStore } from 'pinia';
import http from './http';
import { ref } from 'vue';
import { Response } from '@/types';
import { RouteOption } from '@/router/interface';
import { replaceRoutes, resetRouter } from '@/router/dynamicRoutes';


export interface MenuProps {
  id?: number;
  name: string;
  path: string;
  title?: string;
  icon?: string;
  badge?: number | string;
  target?: '_self' | '_blank';
  link?: string;
  component: string;
  renderMenu?: boolean;
  permission?: string;
  parent?: string;
  children?: MenuProps[];
  cacheable?: boolean;
  view?: string;
}

// 将菜单数据转换为路由数据
const toRoutes = (list: MenuProps[]): RouteOption[] => {
  return list.map((item) => ({
    name: item.name,
    path: item.path,
    component: item.component,
    children: item.children && toRoutes(item.children),
    meta: {
      title: item.title,
      permission: item.permission,
      icon: item.icon,
      renderMenu: item.renderMenu,
      cacheable: item.cacheable,
      href: item.link,
      badge: /^(false|true)$/i.test(String(item.badge)) ? JSON.parse(String(item.badge)) : item.badge,
      target: item.target,
      view: item.view,
    },
  }));
};

export const useMenuStore = defineStore('menu', () => {
  const menuList = ref<MenuProps[]>([]);
  const routesLoaded = ref(false);

  async function getMenuList(userType: string) {
    routesLoaded.value = false; // 在加载前重置
    return http
        .request<MenuProps[], Response<MenuProps[]>>('/menu', 'POST', { userType })
        .then((res) => {
          const { data } = res;
          menuList.value = data;
          const dynamicRoutes = toRoutes(data);
          replaceRoutes(dynamicRoutes, false); // 替换动态路由
          routesLoaded.value = true; // 加载完成后设置为 true
          return data;
        });
  }

  function resetMenu() {
    menuList.value = [];
    routesLoaded.value = false;
    resetRouter(); // 重置路由，移除动态路由
  }

  return {
    menuList,
    getMenuList,
    routesLoaded,
    resetMenu,
  };
});
