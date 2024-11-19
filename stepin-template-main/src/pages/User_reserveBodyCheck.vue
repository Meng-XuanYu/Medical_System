<template>
  <div class="examination-page">
    <h1>体检项目预约</h1>

    <!-- 体检项目列表 -->
    <div v-if="examinations.length > 0">
      <a-table :columns="columns" :data-source="examinations" row-key="examination_id">
        <template #action="{ record }">
          <a-button type="primary" @click="reserveExamination(record)" :disabled="record.isReserved">
            {{ record.isReserved ? '已预约' : '预约' }}
          </a-button>
        </template>
      </a-table>
    </div>
    <div v-else>
      <p>暂无体检项目</p>
    </div>

    <!-- 预约历史 -->
    <div class="reservation-history">
      <h2>预约历史</h2>
      <div v-if="reservations.length > 0">
        <a-table :columns="historyColumns" :data-source="reservations" row-key="reservation_id">
          <template #action="{ record }">
            <a-button type="danger" @click="cancelReservation(record)" v-if="isFutureDate(record.examination_date)">
              取消预约
            </a-button>
            <span v-else>已过期</span>
          </template>
        </a-table>
      </div>
      <div v-else>
        <p>暂无预约记录</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';
import http from "@/store/http";

const user_id = localStorage.getItem('user_id');

const examinations = ref([]);
const reservations = ref([]);

const columns = [
  { title: '体检号', dataIndex: 'examination_id', key: 'examination_id' },
  { title: '体检项目', dataIndex: 'examination_text', key: 'examination_text' },
  { title: '体检日期', dataIndex: 'examination_date', key: 'examination_date' },
  { title: '负责医工号', dataIndex: 'staff_id', key: 'staff_id' },
  {
    title: '操作',
    key: 'action',
    width: 100,
    slots: { customRender: 'action' },
  },
];

const historyColumns = [
  { title: '预约编号', dataIndex: 'reservation_id', key: 'reservation_id' },
  { title: '体检号', dataIndex: 'examination_id', key: 'examination_id' },
  { title: '体检项目', dataIndex: 'examination_text', key: 'examination_text' },
  { title: '体检日期', dataIndex: 'examination_date', key: 'examination_date' },
  {
    title: '操作',
    key: 'action',
    width: 100,
    slots: { customRender: 'action' },
  },
];

function isFutureDate(date) {
  const today = new Date().setHours(0, 0, 0, 0);
  const targetDate = new Date(date).setHours(0, 0, 0, 0);
  return targetDate > today;
}

function fetchExaminations() {
  http.request('/examination/info/', 'get').then(response => {
    examinations.value = response.data.map(item => {
      item.isReserved = false;
      reservations.value.forEach(reservation => {
        if (reservation.examination_id === item.examination_id) {
          item.isReserved = true;
        }
      });
      return item;
    });
  });
}

function fetchReservations() {
  http.request(`/user/examination/info/`, 'get' ).then(response => {
    reservations.value = response.data;
    fetchExaminations();
  });
}

function reserveExamination(record) {
  http.request('/user/examination/reserve/', 'POST_JSON', {
    user_id: user_id,
    examination_id: record.examination_id,
  }).then(() => {
    message.success('预约成功');
    fetchReservations();
  }).catch(() => {
    message.error('预约失败');
  });
}

function cancelReservation(record) {
  http.request('/user/examination/cancel/', 'POST_JSON', {
    user_id: user_id,
    reservation_id: record.reservation_id,
  }).then(() => {
    message.success('取消预约成功');
    fetchReservations();
  }).catch(() => {
    message.error('取消预约失败');
  });
}

onMounted(() => {
  fetchReservations();
});
</script>

<style scoped>
.examination-page {
  padding: 24px;
  min-width: 1190px;
  margin: 0 auto;
  font-family: 'Arial', sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.examination-page h1 {
  text-align: center;
  margin-bottom: 24px;
  font-size: 28px;
  color: #333;
}

.a-table {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.a-table .ant-table-thead > tr > th {
  text-align: center;
  font-weight: bold;
  background-color: #fafafa;
}

.a-table .ant-table-tbody > tr > td {
  text-align: center;
  padding: 12px;
}

.a-table .ant-table-tbody > tr:hover > td {
  background-color: #f5f5f5;
}

.a-button {
  border-radius: 4px;
}

.a-button-primary {
  background-color: #1890ff;
  border-color: #1890ff;
}

.a-button-danger {
  background-color: #ff4d4f;
  border-color: #ff4d4f;
}

.reservation-history {
  margin-top: 40px;
}

.reservation-history h2 {
  margin-bottom: 16px;
  font-size: 24px;
  color: #333;
}
</style>
