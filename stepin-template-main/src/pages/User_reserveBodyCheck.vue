<!-- PhysicalExam.vue -->
<template>
  <div class="physical-exam-page">
    <h1>体检预约</h1>
    <a-form :label-col="{ span: 4 }" :wrapper-col="{ span: 14 }">
      <a-form-item label="选择日期">
        <a-date-picker v-model="selectedDate" :disabled-date="disabledDate" />
      </a-form-item>
      <a-form-item label="选择项目">
        <a-checkbox-group v-model="selectedItems">
          <a-checkbox v-for="item in examItems" :key="item.examination_id" :value="item.examination_id">
            {{ item.examination_name }}
          </a-checkbox>
        </a-checkbox-group>
      </a-form-item>
      <a-form-item wrapper-col="{ offset: 4 }">
        <a-button type="primary" @click="submitAppointment">提交预约</a-button>
      </a-form-item>
    </a-form>

    <h2>已预约体检记录</h2>
    <a-table :columns="columns" :data-source="appointments" row-key="exam_appointment_id"></a-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';

const user = {
  id: 'S1234567',
};

const selectedDate = ref(null);
const selectedItems = ref([]);
const examItems = ref([]);
const appointments = ref([]);

const columns = [
  { title: '预约号', dataIndex: 'exam_appointment_id', key: 'exam_appointment_id' },
  { title: '日期', dataIndex: 'date', key: 'date' },
  { title: '项目', dataIndex: 'items', key: 'items' },
];

function disabledDate(current) {
  // 禁用过去的日期
  return current && current < new Date().setDate(new Date().getDate() - 1);
}

function fetchExamItems() {
  // axios.get('/api/examItems').then(response => {
  //   examItems.value = response.data;
  // });

  // 模拟数据
  examItems.value = [
    { examination_id: 'E01', examination_name: '血常规' },
    { examination_id: 'E02', examination_name: '尿常规' },
    { examination_id: 'E03', examination_name: '心电图' },
  ];
}

function submitAppointment() {
  if (!selectedDate.value || selectedItems.value.length === 0) {
    message.warning('请选择日期和项目');
    return;
  }

  // 调用后端API提交体检预约
  // axios.post('/api/examAppointments', { ... }).then(() => {
  //   message.success('体检预约成功');
  //   fetchAppointments();
  // });

  // 模拟提交成功
  message.success('体检预约成功');
  fetchAppointments();
}

function fetchAppointments() {
  // axios.get(`/api/examAppointments?user_id=${user.id}`).then(response => {
  //   appointments.value = response.data;
  // });

  // 模拟数据
  appointments.value = [
    {
      exam_appointment_id: 'EA001',
      date: '2023-10-15',
      items: '血常规, 尿常规',
    },
  ];
}

onMounted(() => {
  fetchExamItems();
  fetchAppointments();
});
</script>

<style scoped>
.physical-exam-page {
  padding: 24px;
}
</style>
