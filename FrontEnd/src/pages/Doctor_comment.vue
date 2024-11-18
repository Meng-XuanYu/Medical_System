<template>
  <div>
    <h1>患者评价</h1>
    <a-table :columns="columns" :data-source="evaluations" row-key="evaluation_id">
      <template #evaluation="{ text }">
        <span>{{ text }}</span>
      </template>
    </a-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const evaluations = ref([]);

const columns = [
  { title: '评价时间', dataIndex: 'evaluation_time', key: 'evaluation_time' },
  { title: '评价内容', dataIndex: 'evaluation', key: 'evaluation' },
];

function fetchEvaluations() {
  const currentStaffId = 'D1234'; // 从登录信息中获取

  // 调用后端API获取评价信息
  // 示例API调用：
  // axios.get(`/api/doctor/evaluations?staff_id=${currentStaffId}`).then(response => {
  //   evaluations.value = response.data;
  // });

  // 模拟数据
  evaluations.value = [
    {
      evaluation_id: 'E0001',
      evaluation_time: '2023-10-01 10:00:00',
      evaluation: '医生非常专业，态度很好。',
    },
  ];
}

onMounted(() => {
  fetchEvaluations();
});
</script>

<style scoped>
</style>
