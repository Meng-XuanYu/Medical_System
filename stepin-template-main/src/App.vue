<template>
  <a-config-provider :getPopupContainer="getPopupContainer">
    <ThemeProvider is-root v-bind="themeConfig" :apply-style="false">
      <stepin-view
          system-name="航医通"
          logo-src="@/assets/img.png"
          :class="`${contentClass}`"
          :user="user"
          :navMode="navigation"
          :useTabs="useTabs"
          :themeList="themeList"
          v-model:show-setting="showSetting"
          v-model:theme="theme"
          @themeSelect="configTheme"
      >
        <template #headerActions>
          <HeaderActions @showSetting="showSetting = true"/>
        </template>
        <template #pageFooter>
          <PageFooter/>
        </template>
      </stepin-view>
    </ThemeProvider>
  </a-config-provider>
  <login-modal :unless="['/login']"/>
</template>

<script lang="ts" setup>
import {reactive, ref} from 'vue';
import {useRouter} from 'vue-router';
import {useAccountStore, useSettingStore, storeToRefs} from '@/store';
import avatar from '@/assets/avatar.png';
import {PageFooter, HeaderActions} from '@/components/layout';
import {LoginModal} from '@/pages/login';
import {configTheme, themeList} from '@/theme';
import {StepinView, ThemeProvider} from 'stepin';
import {computed} from 'vue';
import {useMenuStore} from '@/store/menu';

const globalusertype = localStorage.getItem('usertype');
useMenuStore().getMenuList(String(globalusertype));
console.log(globalusertype);
console.log(useMenuStore().menuList);

const {logout} = useAccountStore();
const showSetting = ref(false);
const router = useRouter();

router.afterEach((to) => {
  sessionStorage.setItem('last_page', to.fullPath);
});
console.log('hreer');
if (localStorage.getItem('logged') === 'true') {
  console.log('已登录');
  if (localStorage.getItem('usertype') == 'a') {
    const last_page = sessionStorage.getItem('last_page');
    if (last_page != null && !last_page.includes('admin')) {
      console.log('/home');
      router.replace('/home');
    } else {
      console.log(sessionStorage.getItem('last_page') || '/home');
      router.replace(sessionStorage.getItem('last_page') || '/home');
    }
  } else if (localStorage.getItem('usertype') == 'd') {
    const last_page = sessionStorage.getItem('last_page');
    if (last_page != null && !last_page.includes('doctor')) {
      console.log('/home');
      router.replace('/home');
    } else {
      console.log(sessionStorage.getItem('last_page') || '/home');
      router.replace(sessionStorage.getItem('last_page') || '/home');
    }
  } else if (localStorage.getItem('usertype') == 't') {
    const last_page = sessionStorage.getItem('last_page');
    if (last_page != null && !last_page.includes('user') && !last_page.includes('teacher')) {
      console.log('/home');
      router.replace('/home');
    } else {
      console.log(sessionStorage.getItem('last_page') || '/home');
      router.replace(sessionStorage.getItem('last_page') || '/home');
    }
  } else if (localStorage.getItem('usertype') == 's') {
    const last_page = sessionStorage.getItem('last_page');
    if (last_page != null && !last_page.includes('student') && !last_page.includes('user')) {
      console.log('/home');
      router.replace('/home');
    } else {
      console.log(sessionStorage.getItem('last_page') || '/home');
      router.replace(sessionStorage.getItem('last_page') || '/home');
    }
  } else {
    console.log('?');
  }
} else {
  router.replace('/login');
}

const {navigation, useTabs, theme, contentClass} = storeToRefs(useSettingStore());
const themeConfig = computed(() => themeList.find((item) => item.key === theme.value)?.config ?? {});

const user = reactive({
  name: 'admin',
  avatar: avatar,
  usertype: '',
  menuList: [
    {title: '个人中心', key: 'personal', icon: 'UserOutlined', onClick: () => router.push('/personal')},
    {type: 'divider'},
    {
      title: '退出登录',
      key: 'logout',
      icon: 'LogoutOutlined',
      onClick: () => logout().then(() => router.push('/login')),
    },
  ],
});

user.name = localStorage.getItem('username');

function getPopupContainer() {
  return document.querySelector('.stepin-layout');
}
</script>

<style lang="less">
.stepin-view {
  ::-webkit-scrollbar {
    width: 4px;
    height: 4px;
    border-radius: 4px;
    background-color: theme('colors.primary.500');
  }

  ::-webkit-scrollbar-thumb {
    border-radius: 4px;
    background-color: theme('colors.primary.400');

    &:hover {
      background-color: theme('colors.primary.500');
    }
  }

  ::-webkit-scrollbar-track {
    box-shadow: inset 0 0 1px rgba(0, 0, 0, 0);
    border-radius: 4px;
    background: theme('backgroundColor.layout');
  }
}

html {
  height: 100vh;
  overflow-y: hidden;
}

body {
  margin: 0;
  height: 100vh;
  overflow-y: hidden;
}

.stepin-img-checkbox {
@apply transition-transform;

  &:hover {
  @apply scale-105 ~ "-translate-y-[2px]";
  }

  img {
  @apply shadow-low rounded-md transition-transform;
  }
}
</style>
