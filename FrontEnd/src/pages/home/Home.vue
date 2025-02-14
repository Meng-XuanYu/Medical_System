<template>
  <div class="home text-center flex flex-col">
    <div class="transform w-full">

      <div class="tracking-wide slogan text-[2.5rem] xl:text-[4.25rem] font-light leading-tight">
        <span class="font-bold">预约 · 缴费 · 处方</span>
        <br />
        <span class="text-secondary">病历 · 取药 · 医评</span>
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

      <br />
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
import { useRouter } from 'vue-router';
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
    title: '医师评价',
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
  switch (localStorage.getItem('usertype')) {
    case 's':
    case 't':
      router.push('/reserve');
      break;
    case 'a':
      router.push('/admin_doctor');
      break;
    case 'd':
        router.push('/myarrange');
        break;
  }
} else {
  ElMessage.success('请先登录');
}


</script>

<style scoped lang="less">
.page-container {
  background-color: #ffffff; /* 纯白背景 */
  border-radius: 16px; /* 圆角设计，增加柔和感 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05); /* 轻柔阴影，增加层次 */
  padding: 24px; /* 内部留白，确保内容不贴边 */
  margin: 20px auto; /* 居中显示，顶部和底部增加间距 */
  max-width: 1200px; /* 最大宽度，避免内容过宽 */
  transition: box-shadow 0.3s ease; /* 鼠标悬停时的平滑过渡 */
}

.page-container:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); /* 悬停时加深阴影，增加动态效果 */
}

.page-header {
  font-size: 24px; /* 标题字体大小 */
  font-weight: bold; /* 标题加粗 */
  color: #1d4ed8; /* 主色调蓝色 */
  border-bottom: 2px solid #e5e7eb; /* 底部分割线 */
  padding-bottom: 12px; /* 与标题内容间距 */
  margin-bottom: 24px; /* 标题与下方内容间距 */
}

.page-content {
  font-size: 16px; /* 正文字体大小 */
  color: #374151; /* 深灰色字体，提升可读性 */
  line-height: 1.75; /* 行距，改善文本阅读体验 */
}

.page-content a {
  color: #2563eb; /* 链接使用蓝色 */
  text-decoration: none; /* 去掉下划线 */
  font-weight: 500; /* 增加链接文字厚重感 */
  transition: color 0.3s ease; /* 鼠标悬停时平滑过渡 */
}

.page-content a:hover {
  color: #1d4ed8; /* 悬停时链接加深颜色 */
}

.page-footer {
  text-align: center; /* 居中对齐 */
  font-size: 14px; /* 较小字体 */
  color: #9ca3af; /* 浅灰色文本 */
  margin-top: 32px; /* 顶部留白 */
  border-top: 1px solid #e5e7eb; /* 分隔线 */
  padding-top: 16px; /* 内部间距 */
}
</style>


<style scoped lang="less">
.home {
  min-height: max(100vh, 600px);
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #3075e2; /* 中间色，兼具两种蓝色的特点 */
  color: #fff;
  font-family: 'Inter', sans-serif; /* 更现代的字体 */
}

.features-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* 响应式网格 */
  width: 100%;
  max-width: 1200px;
  padding: 20px;
}

.feature-card {
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px; /* 更圆润的设计 */
  padding: 32px;
  text-align: center;
  background: rgba(255, 255, 255, 0.1); /* 半透明背景 */
  backdrop-filter: blur(10px); /* 毛玻璃效果 */
  color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-10px); /* 提升效果 */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  background: rgba(255, 255, 255, 0.3);
}

.feature-card .icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #ffed4a; /* 突出显示的颜色 */
}

.feature-card h3 {
  margin-bottom: 8px;
  font-size: 1.5rem;
  font-weight: bold;
}

.feature-card p {
  margin: 0;
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
}
</style>
