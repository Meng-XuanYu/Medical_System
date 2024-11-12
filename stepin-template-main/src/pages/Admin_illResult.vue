<template>
  <div>
    <h1>诊断信息管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入诊断号、患者身份证号或医工号"
          @search="fetchDiagnoses"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增诊断</a-button>
    </div>
    <a-table :columns="columns" :data-source="diagnoses" row-key="diagnosis_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteDiagnosis(record.diagnosis_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑诊断信息的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
        width="800px"
    >
      <a-form
          :model="currentDiagnosis"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          ref="diagnosisForm"
      >
        <a-form-item label="诊断号" :rules="[{ required: true, message: '请输入诊断号' }]">
          <a-input v-model="currentDiagnosis.diagnosis_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="检查项目" :rules="[{ required: true, message: '请输入检查项目' }]">
          <a-textarea v-model="currentDiagnosis.examination" rows="2" />
        </a-form-item>
        <a-form-item label="检查结果" :rules="[{ required: true, message: '请输入检查结果' }]">
          <a-textarea v-model="currentDiagnosis.examination_result" rows="2" />
        </a-form-item>
        <a-form-item label="参考范围" :rules="[{ required: true, message: '请输入参考范围' }]">
          <a-textarea v-model="currentDiagnosis.reference" rows="2" />
        </a-form-item>
        <a-form-item label="临床诊断" :rules="[{ required: true, message: '请输入临床诊断' }]">
          <a-textarea v-model="currentDiagnosis.clinical_diagnosis" rows="2" />
        </a-form-item>
        <a-form-item label="处方号" :rules="[{ required: true, message: '请输入处方号' }]">
          <a-input v-model="currentDiagnosis.prescription_id" />
        </a-form-item>
        <a-form-item label="诊断时间" :rules="[{ required: true, message: '请选择诊断时间' }]">
          <a-date-picker
              v-model="currentDiagnosis.diagnosis_time"
              show-time
              format="YYYY-MM-DD HH:mm:ss"
          />
        </a-form-item>
        <a-form-item label="患者身份证号" :rules="[{ required: true, message: '请输入身份证号' }]">
          <a-input v-model="currentDiagnosis.id_number" />
        </a-form-item>
        <a-form-item label="预约号" :rules="[{ required: true, message: '请输入预约号' }]">
          <a-input v-model="currentDiagnosis.appointment_id" />
        </a-form-item>
        <a-form-item label="医工号" :rules="[{ required: true, message: '请输入医工号' }]">
          <a-input v-model="currentDiagnosis.staff_id" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const diagnoses = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增诊断');
const isEdit = ref(false);
const currentDiagnosis = reactive({
  diagnosis_id: '',
  examination: '',
  examination_result: '',
  reference: '',
  clinical_diagnosis: '',
  prescription_id: '',
  diagnosis_time: null,
  id_number: '',
  appointment_id: '',
  staff_id: '',
});

const columns = [
  { title: '诊断号', dataIndex: 'diagnosis_id', key: 'diagnosis_id' },
  { title: '检查项目', dataIndex: 'examination', key: 'examination' },
  { title: '检查结果', dataIndex: 'examination_result', key: 'examination_result' },
  { title: '临床诊断', dataIndex: 'clinical_diagnosis', key: 'clinical_diagnosis' },
  { title: '处方号', dataIndex: 'prescription_id', key: 'prescription_id' },
  { title: '诊断时间', dataIndex: 'diagnosis_time', key: 'diagnosis_time' },
  { title: '患者身份证号', dataIndex: 'id_number', key: 'id_number' },
  { title: '医工号', dataIndex: 'staff_id', key: 'staff_id' },
  {
    title: '操作',
    key: 'action',
    fixed: 'right',
    width: 120,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchDiagnoses() {
  // 调用后端API获取诊断信息，支持搜索
  diagnoses.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增诊断';
  isEdit.value = false;
  Object.assign(currentDiagnosis, {
    diagnosis_id: '',
    examination: '',
    examination_result: '',
    reference: '',
    clinical_diagnosis: '',
    prescription_id: '',
    diagnosis_time: null,
    id_number: '',
    appointment_id: '',
    staff_id: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑诊断';
  isEdit.value = true;
  Object.assign(currentDiagnosis, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.diagnosisForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新诊断信息
      message.success('更新诊断信息成功');
    } else {
      // 调用后端API新增诊断
      message.success('新增诊断成功');
    }
    isModalVisible.value = false;
    fetchDiagnoses();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteDiagnosis(diagnosis_id) {
  // 调用后端API删除诊断信息
  message.success('删除诊断信息成功');
  fetchDiagnoses();
}

onMounted(() => {
  fetchDiagnoses();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
