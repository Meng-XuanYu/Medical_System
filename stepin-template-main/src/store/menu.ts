import { defineStore, storeToRefs } from 'pinia';
import http from './http';
import { ref, watch } from 'vue';
import { Response } from '@/types';
import { RouteOption } from '@/router/interface';
import { replaceRoutes, removeRoute } from '@/router/dynamicRoutes';
import { useSettingStore } from './setting';
import { RouteRecordRaw, RouteMeta } from 'vue-router';
import { useAuthStore } from '@/plugins';
import router from '@/router';
import { useLoadingStore } from '@/store';

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

/**
 * 过滤菜单
 * @param routes
 * @param parentPermission
 */
function doMenuFilter(routes: Readonly<RouteRecordRaw[]>, parentPermission?: string) {
  const { hasAuthority } = useAuthStore();

  const setCache = (meta: RouteMeta) => {
    meta._cache = {
      renderMenu: meta.renderMenu,
    };
  };

  routes.forEach((route) => {
    const required = route.meta?.permission ?? parentPermission;
    // if (route.meta?.renderMenu === undefined && required) {
    if (required) {
      route.meta = route.meta ?? {};
      setCache(route.meta);
      route.meta.renderMenu = hasAuthority(route.meta.permission);
    }
    if (route.children) {
      doMenuFilter(route.children, required);
    }
  });
}

/**
 * 重置过滤
 * @param routes
 */
function resetMenuFilter(routes: Readonly<RouteRecordRaw[]>) {
  const resetCache = (meta: RouteMeta) => {
    if (meta._cache) {
      meta.renderMenu = meta._cache?.renderMenu;
    }
    delete meta._cache;
  };
  routes.forEach((route) => {
    if (route.meta) {
      resetCache(route.meta);
    }
    if (route.children) {
      resetMenuFilter(route.children);
    }
  });
}

// 菜单数据转为路由数据
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
      badge: /^(false|true)$/i.test(item.badge + '') ? JSON.parse(item.badge + '') : item.badge,
      target: item.target,
      view: item.view,
    },
  }));
};

export const useMenuStore = defineStore('menu', () => {
  const menuList = ref<MenuProps[]>([]);

  const { filterMenu } = storeToRefs(useSettingStore());

  const checkMenuPermission = () => {
    if (filterMenu.value) {
      doMenuFilter(router.options.routes);
      console.log(router.options.routes);
    } else {
      resetMenuFilter(router.options.routes);
    }
  };

  checkMenuPermission();

  watch(filterMenu, checkMenuPermission);

  async function getMenuList(userType: string) {
    const { setPageLoading } = useLoadingStore();
    setPageLoading(true);

    if (localStorage.getItem('usertype') === 'a') {
      menuList.value = [
        {
          id: 17,
          name: 'admin_4',
          title: '新医师注册',
          path: '/admin_doctor',
          icon: 'UserOutlined',  // 适合医生信息管理
          permission: null,
          component: '@/pages/Admin_Doctor.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 14,
          name: 'admin_1',
          title: '体检项目管理',
          path: '/admin_bodycheck',
          icon: 'AppstoreAddOutlined',  // 适合体检项目管理
          permission: null,
          component: '@/pages/Admin_BodyCheck.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 15,
          name: 'admin_2',
          title: '体检信息管理',
          path: '/admin_bodycheckinfo',
          icon: 'FileTextOutlined',  // 适合体检信息管理
          permission: null,
          component: '@/pages/Admin_BodyCheckInfo.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 16,
          name: 'admin_3',
          title: '医生评价管理',
          path: '/admin_comment',
          icon: 'StarOutlined',  // 适合医生评价管理
          permission: null,
          component: '@/pages/Admin_comment.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 18,
          name: 'admin_5',
          title: '医生安排管理',
          path: '/admin_doctorarrange',
          icon: 'CalendarOutlined',  // 适合医生安排管理
          permission: null,
          component: '@/pages/Admin_DoctorArrange.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 19,
          name: 'admin_6',
          title: '科室信息管理',
          path: '/admin_doctorroom',
          icon: 'ApartmentOutlined',  // 适合科室信息管理
          permission: null,
          component: '@/pages/Admin_DoctorRoom.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 20,
          name: 'admin_7',
          title: '家属信息管理',
          path: '/admin_familys',
          icon: 'TeamOutlined',  // 适合家属信息管理
          permission: null,
          component: '@/pages/Admin_Familys.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 21,
          name: 'admin_8',
          title: '诊断信息管理',
          path: '/admin_illresult',
          icon: 'SolutionOutlined',  // 适合诊断信息管理
          permission: null,
          component: '@/pages/Admin_illResult.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 22,
          name: 'admin_9',
          title: '药品信息管理',
          path: '/admin_medicine',
          icon: 'MedicineBoxOutlined',  // 适合药品信息管理
          permission: null,
          component: '@/pages/Admin_medicine.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 23,
          name: 'admin_10',
          title: '药房信息管理',
          path: '/admin_medicineroom',
          icon: 'ShopOutlined',  // 适合药房信息管理
          permission: null,
          component: '@/pages/Admin_MedicineRoom.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 24,
          name: 'admin_11',
          title: '药品库存管理',
          path: '/admin_medicinestorage',
          icon: 'DatabaseOutlined',  // 适合药品库存管理
          permission: null,
          component: '@/pages/Admin_medicineStorage.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 26,
          name: 'admin_13',
          title: '处方信息管理',
          path: '/admin_prescription',
          icon: 'FileDoneOutlined',  // 适合处方信息管理
          permission: null,
          component: '@/pages/Admin_Prescription.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 27,
          name: 'admin_14',
          title: '预约记录管理',
          path: '/admin_reserverecord',
          icon: 'BookOutlined',  // 适合预约记录管理
          permission: null,
          component: '@/pages/Admin_ReserveRecord.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 28,
          name: 'admin_15',
          title: '用户信息管理',
          path: '/admin_users',
          icon: 'UsergroupAddOutlined',  // 适合用户信息管理
          permission: null,
          component: '@/pages/Admin_Users.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 310,
          name: 'admin_18',
          title: '通知信息管理',
          path: '/admin_notification',
          icon: 'NotificationOutlined',
          permission: null,
          component: '@/pages/Admin_notification.vue',
          renderMenu: true,
          parent: null,
        }
      ];
    } else if (localStorage.getItem('usertype') === 's') {
      menuList.value = [
        {
          id: 3,
          name: 'user_personal',
          title: '个人中心',
          path: '/user_personal',
          icon: 'UserOutlined',  // 适合个人中心
          permission: null,
          component: '@/pages/personal',
          renderMenu: true,
          parent: null,
        },
        {
          id: 4,
          name: 'user_reserve',
          title: '预约挂号',
          path: '/user_reserve',
          icon: 'CalendarOutlined',  // 适合预约挂号
          permission: null,
          component: '@/pages/User_reserve.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 13,
          name: 'user_pay',
          title: '在线缴费',
          path: '/user_pay',
          icon: 'CreditCardOutlined',  // 适合在线缴费
          permission: null,
          component: '@/pages/User_pay.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 5,
          name: 'commentOnDoctor',
          title: '医师评价',
          path: '/user_commentOnDoctor',
          icon: 'StarOutlined',  // 适合评价
          permission: null,
          component: '@/pages/User_commentOnDoctor.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 11,
          name: 'healthDocument',
          title: '健康档案',
          path: '/user_healthDocument',
          icon: 'FileTextOutlined',  // 适合健康档案
          permission: null,
          component: '@/pages/User_healthDocument.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 12,
          name: 'reserveBodyCheck',
          title: '体检预约',
          path: '/user_reserveBodyCheck',
          icon: 'SolutionOutlined',  // 适合体检预约
          permission: null,
          component: '@/pages/User_reserveBodyCheck.vue',
          renderMenu: true,
          parent: null,
        },
      ];
    } else if (localStorage.getItem('usertype') === 'd') {
      menuList.value = [
        {
          id: 44,
          name: 'doctor_1',
          title: '排班查询',
          path: '/doctor_myarrange',
          icon: 'ScheduleOutlined',  // 适合排班查询
          permission: null,
          component: '@/pages/Doctor_MyArrange.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 45,
          name: 'doctor_2',
          title: '预约信息',
          path: '/doctor_myreserved',
          icon: 'AppstoreOutlined',  // 适合预约信息
          permission: null,
          component: '@/pages/Doctor_Reserved.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 46,
          name: 'doctor_3',
          title: '我的评价',
          path: '/doctor_mycomment',
          icon: 'CommentOutlined',  // 适合医师评价
          permission: null,
          component: '@/pages/Doctor_comment.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 47,
          name: 'doctor_4',
          title: '处方开具',
          path: '/doctor_makepre',
          icon: 'FileDoneOutlined',  // 适合处方开具
          permission: null,
          component: '@/pages/Doctor_makePre.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 48,
          name: 'doctor_5',
          title: '患者信息',
          path: '/doctor_patient',
          icon: 'TeamOutlined',  // 适合患者信息
          permission: null,
          component: '@/pages/Doctor_patient.vue',
          renderMenu: true,
          parent: null,
        },
        {
          id: 49,
          name: 'doctor_6',
          title: '患者病历',
          path: '/doctor_illhistory',
          icon: 'BookOutlined',  // 适合患者病历
          permission: null,
          component: '@/pages/Doctor_patientillhistory.vue',
          renderMenu: true,
          parent: null,
        },
      ];
    } else if (localStorage.getItem('usertype') === 't') {
      menuList.value =  [
        {
          id: 3,
          name: 'personal',
          title: '角色中心',
          path: '/user_personal',
          icon: 'UserOutlined',
          permission: null,
          component: '@/pages/personal',
          renderMenu: true,
          parent: null,
          cacheable: true,
        },
        {
          id: 318,
          name: 'family',
          title: '家属管理',
          path: '/teacher_family',
          icon: 'TeamOutlined',  // 适合家属管理
          permission: null,
          component: '@/pages/Teacher_FamilyManage.vue',
          renderMenu: true,
          parent: null,
          cacheable: true,
        },
        {
          id: 4,
          name: 'reserve',
          title: '预约挂号',
          path: '/user_reserve',
          icon: 'CalendarOutlined',
          permission: null,
          component: '@/pages/User_reserve.vue',
          renderMenu: true,
          parent: null,
          cacheable: true,
        },
        {
          id: 13,
          name: 'pay',
          title: '在线缴费',
          path: '/user_pay',
          icon: 'CreditCardOutlined',
          permission: null,
          component: '@/pages/User_pay.vue',
          renderMenu: true,
          parent: null,
          cacheable: true,
        },
        {
          id: 5,
          name: 'commentOnDoctor',
          title: '医师评价',
          path: '/user_commentOnDoctor',
          icon: 'StarOutlined',
          permission: null,
          component: '@/pages/User_commentOnDoctor.vue',
          renderMenu: true,
          parent: null,
          cacheable: true,
        },
        {
          id: 11,
          name: 'healthDocument',
          title: '健康档案',
          path: '/user_healthDocument',
          icon: 'FileTextOutlined',
          permission: null,
          component: '@/pages/User_healthDocument.vue',
          renderMenu: true,
          parent: null,
          cacheable: true,
        },
      ];
    }
    replaceRoutes(toRoutes(menuList.value), false);
    checkMenuPermission();
    setPageLoading(false);
    return menuList.value;
  }

  return {
    menuList,
    getMenuList,
  };
});
