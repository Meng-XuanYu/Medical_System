<script lang="ts" setup>
  import { LogoutOutlined, UserAddOutlined} from '@ant-design/icons-vue';
  import { onMounted } from 'vue';
  import { ThemeProvider, alert } from 'stepin';

  onMounted(() => {
    alert.info(
      `<div class="text-text">
        航医通目前已经推出
        <span class="underline">预约挂号</span>，
        <span class="underline">线上缴费</span>，
        <span class="underline">电子处方</span>，
        <span class="underline">电子病历</span>，
        <span class="underline">取药列表</span>，
        <span class="underline">医师评价</span>
        等功能，欢迎体验。
        <strong>请使用学工号注册登录</strong>。
      </div>`,
      { renderRaw: true, duration: -1 }
    );
  });

  const navList = [
    {
      title: '产品',
      children: [
        {
          title: 'Stepin Template',
          list: ['Stepin Pro', 'Stepin Style', 'Stepin Admin'],
        },
        {
          title: 'Stepin',
          list: ['Stepin Vue', 'Stepin React', 'Stepin Angular'],
        },
      ],
    },
    {
      title: '开发者',
      children: [
        {
          title: 'Developers',
          list: ['Docs', 'Get Started', 'UI Library', 'Community', 'Open Source'],
        },
      ],
    },
    {
      title: '赞助支持',
    },
    {
      title: '商业合作',
      children: [{ title: 'Business', list: ['Contact Us', 'Cooperation', 'Support'] }],
    },
    {
      title: '关于我们',
    },
  ];
</script>
<template>
  <ThemeProvider :color="{ middle: { 'bg-base': '#003f8c' }, primary: { DEFAULT: '#1896ff' } }" :autoAdapt="false">
    <div class="front-view flex flex-col">
      <div class="text-text flex-1">
        <div class="front-header flex items-baseline py-md px-xl">
          <router-link to="/home" class="text-xxl text-text hover:text-text">
            <img src="@/assets/vite.svg" />
            航医通
          </router-link>
          <div
            style="width: calc(100% - 430px)"
            class="front-navigation mx-xl flex overflow-hidden items-center text-lg overflow-ellipsis whitespace-nowrap"
          >
            <div
              :class="`front-nav-item flex items-center cursor-pointer mx-base ${nav.children ? 'with-list' : ''}`"
              v-for="nav in navList"
            >
              <template v-if="!nav.children">
                {{ nav.title }}
              </template>
              <a-popover :mouseEnterDelay="0.1" v-else placement="bottom">
                <div class="front-nav-item-content">
                  {{ nav.title }}
                </div>
                <template #content>
                  <div class="flex">
                    <div class="not-[:first-child]:ml-lg" v-for="group in nav.children">
                      <h3>{{ group.title }}</h3>
                      <div
                        class="cursor-pointer hover:text-text text-subtext font-light py-xs text-lg"
                        v-for="item in group.list"
                      >
                        {{ item }}
                      </div>
                    </div>
                  </div>
                </template>
              </a-popover>
            </div>
          </div>
          <div>
            <router-link
              to="/login"
              class="login-button h-[46px] border-transparent hover:text-text hover:border-transparent text-lg text-text"
            >
              <LogoutOutlined class="mr-xs" />
              登录
            </router-link>
            <router-link
              to="/register"
              class="login-button h-[46px] border-transparent hover:text-text hover:border-transparent text-lg text-text"
            >
              <UserAddOutlined class="mr-xs" />
              注册
            </router-link>
          </div>
        </div>
        <div class="front-content px-xl">
          <router-view />/* 动态插入的页面内容？ */
        </div>
      </div>
    </div>
  </ThemeProvider>
</template>
<style lang="less" scoped>
  @keyframes gradient-animation {
    0% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 30% 70%;
    }
    100% {
      background-position: 0% 50%;
    }
  }

.front-view {
  background: linear-gradient(135deg, #1d4ed8, #3b82f6);/* 符合主页菜单颜色的全局背景 */
  background-size: 400% 400%;
  animation: gradient-animation 5s ease infinite;

    .front-header {
      .front-nav-item {
        &.with-list .front-nav-item-content {
          &:after {
            content: '';
          @apply ~"h-[8px]" ~"w-[8px]" transition-transform ml-2 inline-block border-text border-l-0 border-t-0 border-r-2 border-b-2 border-solid ~"rotate-[-135deg]" translate-y-1/4;
          }
          &:hover {
            &:after {
            @apply ~"rotate-[45deg]" translate-y-0;
            }
          }
        }
      }
    }

    .front-content {
      min-height: calc(100vh - 78px);
      border-radius: 16px; /* 外层容器圆角 */
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 外层容器阴影 */
      overflow: hidden; /* 确保圆角作用到内部内容 */
      background: #3075e2; /* 中间色，兼具两种蓝色的特点 */
    }

  }

  .login-button {
    border: 2px solid white; /* Add white border */
    border-radius: 4px;
    padding: 8px 16px;
  }
</style>
