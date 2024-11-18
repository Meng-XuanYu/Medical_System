<!-- Evaluation.vue -->
<template>
  <div class="evaluation-page">
    <h1>医生评价</h1>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';


const user = {
  id: 'S1234567',
};

const doctors = ref([]);
const selectedDoctor = ref(null);

const evaluationContent = ref('');

function fetchDoctors() {
  // axios.get('/api/doctors').then(response => {
  //   doctors.value = response.data;
  // });

  // 模拟数据
  doctors.value = [
    { staff_id: 'D1001', name: '李医生' },
    { staff_id: 'D1002', name: '王医生' },
  ];
}



onMounted(() => {
  fetchDoctors();
});
</script>

<style scoped>
.evaluation-page {
  padding: 24px;
}
</style>
