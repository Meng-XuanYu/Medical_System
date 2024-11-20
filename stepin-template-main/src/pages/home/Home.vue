<template>
  <div class="home text-center flex flex-col">
    <div class="transform w-full">
      <div class="tracking-wide slogan text-[2.5rem] xl:text-[4.25rem] font-extralight">
        <span class="font-semibold">
          预约 · 缴费 · 处方
        </span>
        <span style="margin-left: 50px;"> </span>
        病历 · 取药 · 医评
      </div>
      <p class="text-subtext text-[1.5rem] xl:text-[1.75rem] font-extralight tracking-wide">
        北京航空航天大学-校医院-在线服务系统
      </p>

      <!-- 六大基础功能介绍栏开始 -->
      <div class="features-grid grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10 px-10">
        <div
            v-for="(feature, index) in features"
            :key="index"
            class="feature-card border border-white rounded-lg p-6 text-white cursor-pointer hover:bg-white hover:text-primary transition"
            @click="goToFeature(feature.route)"
        >
          <div class="icon mb-4">
            <!-- 您可以使用适当的图标库，如 Font Awesome 或自定义 SVG 图标 -->
            <i :class="feature.iconClass" class="text-4xl"></i>
          </div>
          <h3 class="text-2xl font-bold mb-2">{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
      <!-- 六大基础功能介绍栏结束 -->

      <br/>
      <span class="inline-block text-gray-200 text-xl mr-lg">
        <pre>
        北京航空航天大学 数据库课程小组设计
        </pre>
        <button @click="clearCache" class="clear-cache-button">Clear Cache</button>
      </span>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {useRouter} from 'vue-router';
import {ElMessage} from "element-plus";
import http from "@/store/http";

const router = useRouter();

function clearCache() {
  http.request(
      '/logout/',
      'post',
  );
  localStorage.clear();
  sessionStorage.clear();
  ElMessage.success('Cache cleared successfully');
}

const features = [
  {
    title: '预约挂号',
    description: '在线查看医生排班并预约挂号，选择合适时间段就诊。',
    iconClass: 'fas fa-calendar-check', // 图标类名
    route: '/features/appointment', // 路由路径
  },
  {
    title: '候诊查询',
    description: '查看自己的排队信息，实时了解候诊进度。',
    iconClass: 'fas fa-user-clock',
    route: '/features/waiting',
  },
  {
    title: '线上缴费',
    description: '在线缴纳挂号费、药费等费用，方便快捷。',
    iconClass: 'fas fa-credit-card',
    route: '/features/payment',
  },
  {
    title: '预约体检',
    description: '选择体检时间和项目，在线预约年度体检。',
    iconClass: 'fas fa-notes-medical',
    route: '/features/physical-exam',
  },
  {
    title: '医生评价',
    description: '对就诊经历进行评价，帮助提升医疗服务质量。',
    iconClass: 'fas fa-star',
    route: '/features/evaluation',
  },
  {
    title: '健康档案',
    description: '查看体检记录、病历、就诊记录、处方等健康档案。',
    iconClass: 'fas fa-folder-open',
    route: '/features/health-records',
  },
];

function goToFeature(route: string) {
  router.push(route);
}


if (localStorage.getItem('logged') === 'true') {
  console.log('已登录');
  switch (localStorage.getItem('usertype')) {
    case 's':
    case 't':
      router.push('/user_reserve');
      break;
    case 'a':
      router.push('/admin_doctor');
      break;
    case 'd':
      router.push('/doctor_myarrange');
      break;
  }
} else {
  console.log('未登录');
  ElMessage.success('请先登录');
}


</script>

<style scoped lang="less">
.home {
  min-height: max(100vh, 600px);
  margin-top: 20px;
}

.features-grid {
  /* 调整网格布局间距 */
}

.feature-card {
  /* 样式调整 */
  border: 1px solid #fff;
  border-radius: 8px;
  padding: 24px;
  color: #fff;
  text-align: left;
  transition: background-color 0.3s, color 0.3s;
}

.feature-card:hover {
  background-color: #fff;
  color: #1d4ed8; /* 可根据您的主色调调整 */
}

.feature-card .icon {
  /* 图标样式 */
  margin-bottom: 16px;
}

.feature-card h3 {
  margin-bottom: 8px;
}

.feature-card p {
  margin: 0;
}
</style>


