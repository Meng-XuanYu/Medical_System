<!-- Evaluation.vue -->
<template>
  <div class="evaluation-page">
    <h1>医生评价</h1>
    <a-form :label-col="{ span: 4 }" :wrapper-col="{ span: 14 }">
      <a-form-item label="选择医生">
        <a-select v-model="selectedDoctor" style="width: 200px;">
          <a-select-option v-for="doctor in doctors" :key="doctor.staff_id" :value="doctor.staff_id">
            {{ doctor.name }}
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item label="评价内容">
        <a-textarea v-model="evaluationContent" rows="4" />
      </a-form-item>
      <a-form-item wrapper-col="{ offset: 4 }">
        <a-button type="primary" @click="submitEvaluation">提交评价</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';

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

function submitEvaluation() {
  if (!selectedDoctor.value || !evaluationContent.value) {
    message.warning('请选择医生并填写评价内容');
    return;
  }

  // 调用后端API提交评价
  // axios.post('/api/evaluations', { ... }).then(() => {
  //   message.success('评价提交成功');
  //   evaluationContent.value = '';
  // });

  // 模拟提交成功
  message.success('评价提交成功');
  evaluationContent.value = '';
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
