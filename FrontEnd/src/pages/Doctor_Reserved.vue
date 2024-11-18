<template>
  <div>
    <h1>预约记录查询</h1>
    <div class="search-bar">
      <a-date-picker v-model="selectedDate" @change="fetchAppointments" />
      <a-select v-model="selectedTimeSlot" @change="fetchAppointments" placeholder="选择时间段">
        <a-select-option value="上午">上午</a-select-option>
        <a-select-option value="下午">下午</a-select-option>
      </a-select>
    </div>
    <a-table :columns="columns" :data-source="appointments" row-key="appointment_id">
      <template #patient_name="{ record }">
        <span>{{ record.patient_name }}</span>
      </template>
    </a-table>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const appointments = ref([]);
const selectedDate = ref(null);
const selectedTimeSlot = ref('');

const columns = [
  { title: '预约号', dataIndex: 'appointment_id', key: 'appointment_id' },
  { title: '患者姓名', dataIndex: 'patient_name', key: 'patient_name' },
  { title: '患者关系', dataIndex: 'relationship', key: 'relationship' },
  { title: '预约时间', dataIndex: 'appointment_time', key: 'appointment_time' },
];

function fetchAppointments() {
  const currentStaffId = 'D1234'; // 从登录信息中获取

  if (!selectedDate.value || !selectedTimeSlot.value) {
    return;
  }

  // 调用后端API获取预约信息
  // 示例API调用：
  // axios.get('/api/doctor/appointments', {
  //   params: {
  //     staff_id: currentStaffId,
  //     date: selectedDate.value.format('YYYY-MM-DD'),
  //     time_slot: selectedTimeSlot.value,
  //   },
  // }).then(response => {
  //   appointments.value = response.data;
  // });

  // 模拟数据
  appointments.value = [
    {
      appointment_id: 'A0001',
      patient_name: '张三',
      relationship: '本人',
      appointment_time: selectedDate.value.format('YYYY-MM-DD') + ' ' + selectedTimeSlot.value,
    },
    {
      appointment_id: 'A0002',
      patient_name: '李四',
      relationship: '家属',
      appointment_time: selectedDate.value.format('YYYY-MM-DD') + ' ' + selectedTimeSlot.value,
    },
  ];
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}
</style>
