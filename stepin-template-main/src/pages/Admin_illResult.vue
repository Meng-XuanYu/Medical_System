<template>
  <div class="admin-page">
    <h1 class="title">诊断管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入诊断号、患者身份证号、预约号"
          @search="fetchDiagnoses"
          enter-button
          class="search-input"
      />
      <a-button type="primary" @click="showAddModal" class="add-button">
        <template #icon>
          <PlusOutlined />
        </template>
        新增诊断
      </a-button>
    </div>
    <a-table v-bind="$attrs" :columns="columns" :dataSource="diagnoses" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'diagnosis_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'examination'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'examination_result'" class="type3">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'reference'" class="type4">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'clinical_diagnosis'" class="type5">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'prescription_id'" class="type6">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'diagnosis_time'" class="type7">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'appointment_id'" class="type8">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'staff_id'" class="type9">
          {{ text }}
        </div>
        <template v-else-if="column.dataIndex === 'edit'">
          <a-button type="link" @click="handleEdit(record)" class="edit-button">
            <EditOutlined />
            编辑
          </a-button>
        </template>
        <template v-else-if="column.dataIndex === 'delete'">
          <a-button type="link" @click="handleDelete(record)" class="delete-button">
            <DeleteOutlined />
            删除
          </a-button>
        </template>
        <div v-else class="text-subtext">
          {{ text }}
        </div>
      </template>
    </a-table>

    <div v-if="isModalVisible" class="floating-modal" ref="modal">
      <div class="modal-header">
        <span>{{ modalTitle }}</span>
        <a-button type="link" @click="handleCancel">关闭</a-button>
      </div>
      <a-form :model="currentDiagnosis" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }" ref="diagnosisForm" class="my-form">
        <a-form-item label="诊断号" :rules="[{ required: true, message: '请输入诊断号' }]">
          <a-input v-model:value="currentDiagnosis.diagnosis_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="检查项目" :rules="[{ required: true, message: '请输入检查项目' }]">
          <a-input v-model:value="currentDiagnosis.examination" />
        </a-form-item>
        <a-form-item label="检查结果" :rules="[{ required: true, message: '请输入检查结果' }]">
          <a-input v-model:value="currentDiagnosis.examination_result" />
        </a-form-item>
        <a-form-item label="参考范围" :rules="[{ required: true, message: '请输入参考范围' }]">
          <a-input v-model:value="currentDiagnosis.reference" />
        </a-form-item>
        <a-form-item label="临床诊断" :rules="[{ required: true, message: '请输入临床诊断' }]">
          <a-input v-model:value="currentDiagnosis.clinical_diagnosis" />
        </a-form-item>
        <a-form-item label="处方号" :rules="[{ required: true, message: '请输入处方号' }]">
          <a-input v-model:value="currentDiagnosis.prescription_id" />
        </a-form-item>
        <a-form-item label="诊断时间" :rules="[{ required: true, message: '请输入诊断时间' }]">
          <a-date-picker v-model:value="currentDiagnosis.diagnosis_time" />
        </a-form-item>
        <a-form-item label="预约号" :rules="[{ required: true, message: '请输入预约号' }]">
          <a-input v-model:value="currentDiagnosis.appointment_id" />
        </a-form-item>
        <a-form-item label="医工号" :rules="[{ required: true, message: '请输入医工号' }]">
          <a-input v-model:value="currentDiagnosis.staff_id" />
        </a-form-item>
        <div class="modal-actions">
          <a-button @click="handleOk" type="primary">确认</a-button>
          <a-button @click="handleCancel">取消</a-button>
        </div>
      </a-form>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import http from "@/store/http";

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
  diagnosis_time: '',
  appointment_id: '',
  staff_id: ''
});

const columns = [
  { title: '诊断号', dataIndex: 'diagnosis_id', key: 'diagnosis_id' },
  { title: '检查项目', dataIndex: 'examination', key: 'examination' },
  { title: '检查结果', dataIndex: 'examination_result', key: 'examination_result' },
  { title: '参考范围', dataIndex: 'reference', key: 'reference' },
  { title: '临床诊断', dataIndex: 'clinical_diagnosis', key: 'clinical_diagnosis' },
  { title: '处方号', dataIndex: 'prescription_id', key: 'prescription_id' },
  { title: '诊断时间', dataIndex: 'diagnosis_time', key: 'diagnosis_time' },
  { title: '预约号', dataIndex: 'appointment_id', key: 'appointment_id' },
  { title: '医工号', dataIndex: 'staff_id', key: 'staff_id' },
  {
    title: '操作',
    dataIndex: 'edit',
    key: 'edit',
    width: 100,
  },
  {
    title: '',
    dataIndex: 'delete',
    key: 'delete',
    width: 100,
  }
];

function fetchDiagnoses() {
  http.request('/diagnosis/all/', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    diagnoses.value = response.data;
  });
}

function showAddModal() {
  modalTitle.value = '新增诊断';
  isEdit.value = false;
  Object.assign(currentDiagnosis, { diagnosis_id: '', examination: '', examination_result: '', reference: '', clinical_diagnosis: '', prescription_id: '', diagnosis_time: '', appointment_id: '', staff_id: '' });
  isModalVisible.value = true;
}

function handleEdit(record: any) {
  modalTitle.value = '编辑诊断';
  isEdit.value = true;
  Object.assign(currentDiagnosis, record);
  isModalVisible.value = true;
}

async function handleOk() {
  if (isEdit.value) {
    try {
      await http.request('/diagnosis/update/', 'POST_JSON', { ...currentDiagnosis });
      message.success('编辑诊断信息成功');
    } finally {
      isModalVisible.value = false;
      fetchDiagnoses();
    }
  } else {
    try {
      await http.request('/diagnosis/add/', 'POST_JSON', { ...currentDiagnosis });
      message.success('新增诊断信息成功');
    } finally {
      isModalVisible.value = false;
      fetchDiagnoses();
    }
  }
}

function handleCancel() {
  isModalVisible.value = false;
}

function handleDelete(record: any) {
  http.request('/diagnosis/delete/', 'POST_JSON', { diagnosis_id: record.diagnosis_id });
  message.success('删除诊断信息成功');
  fetchDiagnoses();
}

onMounted(() => {
  fetchDiagnoses();
});
</script>

<style>
.admin-page {
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
  font-family: 'Arial', sans-serif;
}

.title {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
  text-shadow: 1px 1px 2px #aaa;
}

.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.search-input {
  width: 800px;
  border-radius: 4px;
  border: 1px solid #ccc;
  padding: 8px;
}

.add-button {
  background-color: #1890ff;
  color: white;
  border-radius: 4px;
  padding: 8px 16px;
  font-weight: bold;
  height: 40px;
}

.add-button:hover {
  background-color: #40a9ff;
}

.mytable {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.type1 {
  font-weight: bold;
  color: #1890ff;
}

.type2 {

  color: #52c41a;
}

.type3 {

  color: #faad14;
}

.type4 {

  color: #eb2f96;
}

.edit-button {
  color: #1890ff;
}

.delete-button {
  color: #ff4d4f;
}

.floating-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 400px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 999;
  padding: 20px;
  overflow: hidden;
  cursor: move;

}

.modal-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  cursor: move;
  font-size: 18px;
  font-weight: bold;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.my-form {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.my-form .ant-form-item {
  margin-bottom: 16px;
}

.date-select-container {
  display: flex;
  gap: 10px;
}

.date-select {
  width: 100px;
}

.text-subtext {
  color: #888;
}
</style>