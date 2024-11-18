<template>
  <div class="appointment-page">
    <h1 class="page-title">预约挂号</h1>
    <div class="doctor-selection">
      <a-form :layout="'inline'">
        <a-form-item label="选择科室">
          <a-select v-model="selectedDepartment" @change="fetchDoctors" style="width: 200px;">
            <a-select-option v-for="dept in departments" :key="dept.department_id" :value="dept.department_id">
              {{ dept.department_name }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="选择医生">
          <a-select v-model="selectedDoctor" @change="fetchSchedules" style="width: 200px;">
            <a-select-option v-for="doctor in doctors" :key="doctor.staff_id" :value="doctor.staff_id">
              {{ doctor.name }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="选择日期">
          <a-date-picker v-model="selectedDate" style="width: 200px;" @change="fetchSchedules" :get-popup-container="(triggerNode) =>triggerNode.parentNode">
          </a-date-picker>
        </a-form-item>
      </a-form>
    </div>
    <div class="schedule-selection" v-if="schedules.length > 0">
      <h2>可预约时间段</h2>
      <a-list
          :grid="{ gutter: 16, column: 4 }"
          :dataSource="timeSlots"
          bordered
      >
        <template #renderItem="{ item }">
          <a-list-item>
            <a-card
                :title="item.label"
                :hoverable="!isFullBooked(item.value)"
                :class="{ 'full-booked': isFullBooked(item.value) }"
                @click="selectTimeSlot(item.value)"
            >
              <p v-if="isFullBooked(item.value)">预约已满</p>
              <p v-else>可预约</p>
            </a-card>
          </a-list-item>
        </template>
      </a-list>
    </div>
    <div class="appointment-records">
      <h2>我的预约记录</h2>
      <a-table :columns="columns" :dataSource="appointments" row-key="appointment_id">
        <template #status="{ text }">
          <a-tag :color="text === '未完成' ? 'blue' : 'green'">{{ text }}</a-tag>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';

const user = reactive({
  id: 'S1234567',
  name: '张学生',
});

const departments = ref([]);
const doctors = ref([]);
const schedules = ref([]);
const appointments = ref([]);

const selectedDepartment = ref(null);
const selectedDoctor = ref(null);
const selectedDate = ref(null);
const selectedTimeSlot = ref(null);

const timeSlots = [
  { label: '上午 8:00 - 10:00', value: '8-10' },
  { label: '上午 10:00 - 11:30', value: '10-11:30' },
  { label: '下午 13:30 - 15:30', value: '13:30-15:30' },
  { label: '下午 15:30 - 17:30', value: '15:30-17:30' },
];

const columns = [
  { title: '预约号', dataIndex: 'appointment_id', key: 'appointment_id' },
  { title: '医生', dataIndex: 'doctor_name', key: 'doctor_name' },
  { title: '科室', dataIndex: 'department_name', key: 'department_name' },
  { title: '预约日期', dataIndex: 'date', key: 'date' },
  { title: '时间段', dataIndex: 'time_slot', key: 'time_slot' },
  { title: '状态', dataIndex: 'status', key: 'status', scopedSlots: { customRender: 'status' } },
];

function fetchDepartments() {
  departments.value = [
    { department_id: 'D01', department_name: '内科' },
    { department_id: 'D02', department_name: '外科' },
  ];
}

function fetchDoctors() {
  if (!selectedDepartment.value) return;
  doctors.value = [
    { staff_id: 'D1001', name: '李医生' },
    { staff_id: 'D1002', name: '王医生' },
  ];
}

function fetchSchedules() {
  if (!selectedDoctor.value || !selectedDate.value) return;
  const dateStr = selectedDate.value.format('YYYY-MM-DD');
  schedules.value = [
    { schedule_id: 'S001', date: dateStr, time_slot: '8-10' },
    { schedule_id: 'S002', date: dateStr, time_slot: '10-11:30' },
  ];
}

function isFullBooked(timeSlot) {
  return Math.random() < 0.2;
}

function selectTimeSlot(timeSlot) {
  if (isFullBooked(timeSlot)) {
    message.warning('该时间段预约人数已满，请选择其他时间段');
    return;
  }

  const hasPendingAppointment = appointments.value.some(app => app.status === '未完成');
  if (hasPendingAppointment) {
    message.warning('您有未完成的预约，无法再次预约');
    return;
  }

  selectedTimeSlot.value = timeSlot;
  message.success('预约成功');
  fetchAppointments();
}

function fetchAppointments() {
  appointments.value = [
    {
      appointment_id: 'A001',
      doctor_name: '李医生',
      department_name: '内科',
      date: '2023-10-10',
      time_slot: '8-10',
      status: '未完成',
    },
  ];
}

onMounted(() => {
  fetchDepartments();
  fetchAppointments();
});
</script>

<style scoped>
.appointment-page {
  padding: 24px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.page-title {
  font-size: 24px;
  color: #1890ff;
  text-align: center;
  margin-bottom: 24px;
}

.doctor-selection {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
}

.schedule-selection {
  margin-bottom: 24px;
}

.full-booked {
  pointer-events: none;
  opacity: 0.5;
}

.appointment-records {
  margin-top: 24px;
}

a-card {
  transition: transform 0.3s;
}

a-card:hover {
  transform: scale(1.05);
}

a-tag.blue {
  background-color: #1890ff;
  color: white;
}

a-tag.green {
  background-color: #52c41a;
  color: white;
}
</style>