<!-- WaitingQueue.vue -->
<template>
  <div class="waiting-queue-page">
    <h1>候诊查询</h1>
    <div v-if="currentAppointment">
      <p>您预约了 {{ currentAppointment.date }} {{ currentAppointment.time_slot }} 的 {{ currentAppointment.doctor_name }} 医生</p>
      <p>当前前方还有 <strong>{{ peopleAhead }}</strong> 人</p>
    </div>
    <div v-else>
      <p>当前不存在预约</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user = {
  id: 'S1234567',
};

const currentAppointment = ref(null);
const peopleAhead = ref(0);

function fetchCurrentAppointment() {
  // axios.get(`/api/appointments/current?user_id=${user.id}`).then(response => {
  //   currentAppointment.value = response.data.appointment;
  //   peopleAhead.value = response.data.people_ahead;
  // });

  // 模拟数据
  currentAppointment.value = {
    appointment_id: 'A001',
    doctor_name: '李医生',
    date: '2023-10-10',
    time_slot: '8-10',
  };
  peopleAhead.value = 2;
}

onMounted(() => {
  fetchCurrentAppointment();
});
</script>

<style scoped>
.waiting-queue-page {
  padding: 24px;
}
</style>
