<template>
  <div>
    <h1>我的排班</h1>
    <a-table :columns="columns" :data-source="schedules" row-key="schedule_id">
      <template #department="{ text }">
        <span>{{ text }}</span>
      </template>
    </a-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const schedules = ref([]);

const columns = [
  { title: '排班号', dataIndex: 'schedule_id', key: 'schedule_id' },
  { title: '排班日期', dataIndex: 'schedule_date', key: 'schedule_date' },
  { title: '时间段', dataIndex: 'schedule_time', key: 'schedule_time' },
  { title: '科室名称', dataIndex: 'department_name', key: 'department_name' },
];

function fetchSchedules() {
  // 获取当前医生的医工号
  const currentStaffId = 'D1234'; // 应从登录信息中获取

  // 调用后端API获取排班信息
  // 示例API调用：
  // axios.get(`/api/doctor/schedules?staff_id=${currentStaffId}`).then(response => {
  //   schedules.value = response.data;
  // });

  // 模拟数据
  schedules.value = [
    {
      schedule_id: 'S0001',
      schedule_date: '2023-10-01',
      schedule_time: '上午',
      department_name: '内科',
    },
    {
      schedule_id: 'S0002',
      schedule_date: '2023-10-02',
      schedule_time: '下午',
      department_name: '外科',
    },
  ];
}

onMounted(() => {
  fetchSchedules();
});
</script>

<style scoped>
</style>
