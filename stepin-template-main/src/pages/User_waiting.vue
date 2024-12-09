<template>
  <div class="waiting-list">
    <h1>候诊查询</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-if="appointment">
        <p>当前存在未完成的预约记录</p>
        <p>前方有 {{ appointment.waitingCount }} 个人</p>
        <p v-if="!appointment.paid">请先去缴费</p>
      </div>
      <div v-else>
        <p>当前不存在未完成的预约</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const loading = ref(true);
const appointment = ref(null);

async function fetchAppointment() {
  try {
    const response = await axios.get('/api/appointments/waiting');
    if (response.data && response.data.waitingCount !== undefined) {
      appointment.value = response.data;
    } else {
      appointment.value = null;
    }
  } catch (error) {
    console.error('Error fetching appointment:', error);
    appointment.value = null;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchAppointment();
});
</script>

<style scoped>
.waiting-list {
  padding: 24px;
}
</style>