<template>
  <div>
    <h1>处方管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="patientIdNumber"
          placeholder="请输入患者身份证号"
          @search="fetchPrescriptions"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">开具处方</a-button>
    </div>
    <a-table :columns="columns" :data-source="prescriptions" row-key="prescription_id">
      <template #action="{ record }">
        <a-button type="link" @click="viewPrescription(record.prescription_id)">查看详情</a-button>
      </template>
    </a-table>

    <!-- 开具处方的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        title="开具处方"
        @ok="handleOk"
        @cancel="handleCancel"
        width="800px"
    >
      <a-form
          :model="currentPrescription"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          ref="prescriptionForm"
      >
        <a-form-item label="诊断号" :rules="[{ required: true, message: '请输入诊断号' }]">
          <a-input v-model="currentPrescription.diagnosis_id" />
        </a-form-item>
        <a-form-item label="药品" :rules="[{ required: true, message: '请选择药品' }]">
          <a-select v-model="currentPrescription.drug_id" :options="drugOptions" />
        </a-form-item>
        <a-form-item label="药品数量" :rules="[{ required: true, message: '请输入药品数量' }]">
          <a-input-number v-model="currentPrescription.drug_amount" :min="1" />
        </a-form-item>
        <a-form-item label="用法用量" :rules="[{ required: true, message: '请输入用法用量' }]">
          <a-textarea v-model="currentPrescription.usage" rows="2" />
        </a-form-item>
        <a-form-item label="注意事项">
          <a-textarea v-model="currentPrescription.precautions" rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 处方详情模态框 -->
    <a-modal
        v-model:visible="isDetailModalVisible"
        title="处方详情"
        @cancel="handleDetailCancel"
        footer={null}
    >
      <a-table :columns="detailColumns" :data-source="prescriptionDetails" row-key="drug_id" />
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { message } from 'ant-design-vue';

const patientIdNumber = ref('');
const prescriptions = ref([]);
const isModalVisible = ref(false);
const isDetailModalVisible = ref(false);
const currentPrescription = reactive({
  prescription_id: '',
  diagnosis_id: '',
  drug_id: '',
  drug_amount: 1,
  usage: '',
  precautions: '',
});

const prescriptionDetails = ref([]);

const drugOptions = ref([
  // 调用后端API获取药品列表
  // 示例：
  // axios.get('/api/drugs').then(response => {
  //   drugOptions.value = response.data.map(drug => ({
  //     label: drug.drug_name,
  //     value: drug.drug_id,
  //   }));
  // });

  // 模拟数据
  { label: '阿司匹林', value: 'DR001' },
  { label: '布洛芬', value: 'DR002' },
]);

const columns = [
  { title: '处方号', dataIndex: 'prescription_id', key: 'prescription_id' },
  { title: '诊断号', dataIndex: 'diagnosis_id', key: 'diagnosis_id' },
  { title: '开具时间', dataIndex: 'create_time', key: 'create_time' },
  {
    title: '操作',
    key: 'action',
    width: 100,
    scopedSlots: { customRender: 'action' },
  },
];

const detailColumns = [
  { title: '药品名称', dataIndex: 'drug_name', key: 'drug_name' },
  { title: '数量', dataIndex: 'drug_amount', key: 'drug_amount' },
  { title: '用法用量', dataIndex: 'usage', key: 'usage' },
  { title: '注意事项', dataIndex: 'precautions', key: 'precautions' },
];

function fetchPrescriptions() {
  if (!patientIdNumber.value) return;

  // 调用后端API获取处方列表
  // axios.get(`/api/doctor/prescriptions?id_number=${patientIdNumber.value}`).then(response => {
  //   prescriptions.value = response.data;
  // });

  // 模拟数据
  prescriptions.value = [
    {
      prescription_id: 'P0001',
      diagnosis_id: 'D0001',
      create_time: '2023-10-01 10:00:00',
    },
  ];
}

function showAddModal() {
  Object.assign(currentPrescription, {
    prescription_id: '',
    diagnosis_id: '',
    drug_id: '',
    drug_amount: 1,
    usage: '',
    precautions: '',
  });
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.prescriptionForm;
  form.validateFields().then(async () => {
    // 调用后端API新增处方
    message.success('开具处方成功');
    isModalVisible.value = false;
    fetchPrescriptions();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function viewPrescription(prescriptionId) {
  // 调用后端API获取处方详情
  // axios.get(`/api/doctor/prescription/${prescriptionId}`).then(response => {
  //   prescriptionDetails.value = response.data;
  //   isDetailModalVisible.value = true;
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
  isDetailModalVisible.value = true;
}

function handleDetailCancel() {
  isDetailModalVisible.value = false;
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}
</style>
