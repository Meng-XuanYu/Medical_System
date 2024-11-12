<template>
  <div>
    <h1>患者信息查询</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入患者身份证号或学工号"
          @search="fetchPatientInfo"
          enter-button
      />
    </div>
    <div v-if="patient">
      <h2>基本信息</h2>
      <p>姓名：{{ patient.name }}</p>
      <p>身份证号：{{ patient.id_number }}</p>

      <h2>病历和就诊记录</h2>
      <a-table :columns="diagnosisColumns" :data-source="diagnoses" row-key="diagnosis_id">
        <template #action="{ record }">
          <a-button type="link" @click="viewPrescription(record.prescription_id)">查看处方</a-button>
        </template>
      </a-table>
    </div>

    <!-- 处方详情模态框 -->
    <a-modal
        v-model:visible="isPrescriptionModalVisible"
        title="处方详情"
        @cancel="handlePrescriptionCancel"
        footer={null}
    >
      <a-table :columns="prescriptionColumns" :data-source="prescriptionDetails" row-key="drug_id" />
    </a-modal>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const searchText = ref('');
const patient = ref(null);
const diagnoses = ref([]);
const prescriptionDetails = ref([]);
const isPrescriptionModalVisible = ref(false);

const diagnosisColumns = [
  { title: '诊断号', dataIndex: 'diagnosis_id', key: 'diagnosis_id' },
  { title: '检查项目', dataIndex: 'examination', key: 'examination' },
  { title: '检查结果', dataIndex: 'examination_result', key: 'examination_result' },
  { title: '临床诊断', dataIndex: 'clinical_diagnosis', key: 'clinical_diagnosis' },
  { title: '诊断时间', dataIndex: 'diagnosis_time', key: 'diagnosis_time' },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
];

const prescriptionColumns = [
  { title: '药品名称', dataIndex: 'drug_name', key: 'drug_name' },
  { title: '数量', dataIndex: 'drug_amount', key: 'drug_amount' },
  { title: '用法用量', dataIndex: 'usage', key: 'usage' },
  { title: '注意事项', dataIndex: 'precautions', key: 'precautions' },
];

function fetchPatientInfo() {
  if (!searchText.value) return;

  // 调用后端API获取患者信息和诊断记录
  // 示例API调用：
  // axios.get(`/api/doctor/patient?search=${searchText.value}`).then(response => {
  //   patient.value = response.data.patient;
  //   diagnoses.value = response.data.diagnoses;
  // });

  // 模拟数据
  patient.value = {
    id: 'U1234567',
    name: '王五',
    id_number: '123456789012345678',
  };

  diagnoses.value = [
    {
      diagnosis_id: 'D0001',
      examination: '血常规',
      examination_result: '正常',
      clinical_diagnosis: '健康',
      diagnosis_time: '2023-10-01 09:00:00',
      prescription_id: 'P0001',
    },
  ];
}

function viewPrescription(prescriptionId) {
  // 调用后端API获取处方详情
  // 示例API调用：
  // axios.get(`/api/doctor/prescription/${prescriptionId}`).then(response => {
  //   prescriptionDetails.value = response.data;
  //   isPrescriptionModalVisible.value = true;
  // });

  // 模拟数据
  prescriptionDetails.value = [
    {
      drug_id: 'DR001',
      drug_name: '阿司匹林',
      drug_amount: 10,
      usage: '每日一次，每次一片',
      precautions: '饭后服用',
    },
  ];
  isPrescriptionModalVisible.value = true;
}

function handlePrescriptionCancel() {
  isPrescriptionModalVisible.value = false;
}
</script>

<style scoped>
.search-bar {
  margin-bottom: 16px;
}
</style>
