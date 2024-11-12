import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    redirect: '/home',
    meta: {
      title: '首页',
      renderMenu: false,
      icon: 'CreditCardOutlined',
    },
  },
  {
    path: '/front',
    name: '前端',
    meta: {
      renderMenu: false,
    },
    component: () => import('@/components/layout/FrontView.vue').then(m => m.default || m),
    children: [
      {
        path: '/home',
        name: '首页',
        meta: {
          view: 'blank',
        },
        component: () => import('@/pages/home').then(m => m.default || m),
      },
      {
        path: '/login',
        name: '登录',
        meta: {
          icon: 'LoginOutlined',
          view: 'blank',
          target: '_blank',
          cacheable: false,
        },
        component: () => import('@/pages/login').then(m => m.default || m),
      },

      {
        path: '/register',
        name: '注册',
        meta: {
          view: 'blank',
        },
        component: () => import('@/pages/register').then(m => m.default || m),
      },
      {
        path: '/features/appointment',
        name: 'Appointment',
        meta: {
          view: 'blank',
        },
        component: () => import('@/views/features/Appointment.vue').then(m => m.default || m),
      },
      {
        path: '/features/waiting',
        meta: {
          view: 'blank',
        },
        component: () => import('@/views/features/Waiting.vue').then(m => m.default || m),
      },
      {
        path: '/features/payment',
        meta: {
          view: 'blank',
        },
        component: () => import('@/views/features/Payment.vue').then(m => m.default || m),
      },
      {
        path: '/features/physical-exam',
        meta: {
          view: 'blank',
        },
        component: () => import('@/views/features/PhysicalExam.vue').then(m => m.default || m),
      },
      {
        path:'/features/evaluation',
        meta: {
          view: 'blank',
        },
        component: () => import('@/views/features/Evaluation.vue').then(m => m.default || m),
      },
      {
        path: '/features/health-records',
        meta: {
          view: 'blank',
        },
        component: () => import('@/views/features/HealthRecords.vue').then(m => m.default || m),
      }
    ],
  },
  {
    path: '/403',
    name: '403',
    props: true,
    meta: {
      renderMenu: false,
    },
    component: () => import('@/pages/Exp403.vue').then(m => m.default || m),
  },
  {
    path: '/:pathMatch(.*)*',
    name: '404',
    props: true,
    meta: {
      icon: 'CreditCardOutlined',
      renderMenu: false,
      cacheable: false,
      _is404Page: true,
    },
    component: () => import('@/pages/Exp404.vue').then(m => m.default || m),
  },
];

export default routes;
