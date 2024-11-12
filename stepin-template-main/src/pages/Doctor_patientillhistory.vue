<template>
  <div>
    <h1>病历管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="patientIdNumber"
          placeholder="请输入患者身份证号"
          @search="fetchMedicalRecords"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增病历</a-button>
    </div>
    <a-table :columns="columns" :data-source="medicalRecords" row-key="medical_record_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑病历的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
        width="800px"
    >
      <a-form
          :model="currentMedicalRecord"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          ref="medicalRecordForm"
      >
        <a-form-item label="患者身份证号" :rules="[{ required: true, message: '请输入身份证号' }]">
          <a-input v-model="currentMedicalRecord.id_number" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="主诉" :rules="[{ required: true, message: '请输入主诉' }]">
          <a-textarea v-model="currentMedicalRecord.chief_complaint" rows="2" />
        </a-form-item>
        <a-form-item label="现病史">
          <a-textarea v-model="currentMedicalRecord.present_illness_history" rows="2" />
        </a-form-item>
        <a-form-item label="既往史">
          <a-textarea v-model="currentMedicalRecord.past_history" rows="2" />
        </a-form-item>
        <a-form-item label="过敏史">
          <a-textarea v-model="currentMedicalRecord.allergy_history" rows="2" />
        </a-form-item>
        <a-form-item label="体格检查">
          <a-textarea v-model="currentMedicalRecord.physical_examination" rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { message } from 'ant-design-vue';

const patientIdNumber = ref('');
const medicalRecords = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增病历');
const isEdit = ref(false);
const currentMedicalRecord = reactive({
  medical_record_id: '',
  id_number: '',
  chief_complaint: '',
  present_illness_history: '',
  past_history: '',
  allergy_history: '',
  physical_examination: '',
  create_time: null,
  staff_id: '',
});

const columns = [
  { title: '病历号', dataIndex: 'medical_record_id', key: 'medical_record_id' },
  { title: '创建时间', dataIndex: 'create_time', key: 'create_time' },
  { title: '主诉', dataIndex: 'chief_complaint', key: 'chief_complaint' },
  {
    title: '操作',
    key: 'action',
    width: 80,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchMedicalRecords() {
  if (!patientIdNumber.value) return;

  // 调用后端API获取病历信息
  // 示例API调用：
  // axios.get(`/api/doctor/medicalRecords?id_number=${patientIdNumber.value}`).then(response => {
  //   medicalRecords.value = response.data;
  // });

  // 模拟数据
  medicalRecords.value = [
    {
      medical_record_id: 'MR0001',
      id_number: patientIdNumber.value,
      chief_complaint: '头痛三天',
      create_time: '2023-10-01 09:00:00',
      staff_id: 'D1234',
    },
  ];
}

function showAddModal() {
  modalTitle.value = '新增病历';
  isEdit.value = false;
  Object.assign(currentMedicalRecord, {
    medical_record_id: '',
    id_number: patientIdNumber.value,
    chief_complaint: '',
    present_illness_history: '',
    past_history: '',
    allergy_history: '',
    physical_examination: '',
    create_time: null,
    staff_id: 'D1234', // 从登录信息中获取
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑病历';
  isEdit.value = true;
  Object.assign(currentMedicalRecord, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.medicalRecordForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新病历信息
      message.success('更新病历信息成功');
    } else {
      // 调用后端API新增病历
      message.success('新增病历成功');
    }
    isModalVisible.value = false;
    fetchMedicalRecords();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}
</style>
