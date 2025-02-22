<template>
  <div class="admin-page">
    <h1 class="title">处方管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入处方号、诊断号、药品号"
          @search="fetchPrescriptions"
          enter-button
          class="search-input"
      />
      <a-button type="primary" @click="showAddModal" class="add-button">
        <template #icon>
          <PlusOutlined />
        </template>
        新增处方
      </a-button>
    </div>
    <a-table v-bind="$attrs" :columns="columns" :dataSource="prescriptions" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'prescription_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'diagnosis_id'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'drug_id'" class="type3">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'drug_amount'" class="type4">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'usage'" class="type5">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'precautions'" class="type6">
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
      <a-form :model="currentPrescription" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }" ref="prescriptionForm" class="my-form">
        <a-form-item label="处方号" :rules="[{ required: true, message: '请输入处方号' }]">
          <a-input v-model:value="currentPrescription.prescription_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="诊断号" :rules="[{ required: true, message: '请输入诊断号' }]">
          <a-input v-model:value="currentPrescription.diagnosis_id" />
        </a-form-item>
        <a-form-item label="药品号" :rules="[{ required: true, message: '请输入药品号' }]">
          <a-input v-model:value="currentPrescription.drug_id" />
        </a-form-item>
        <a-form-item label="药品数量" :rules="[{ required: true, message: '请输入药品数量' }]">
          <a-input v-model:value="currentPrescription.drug_amount" />
        </a-form-item>
        <a-form-item label="用法用量" :rules="[{ required: true, message: '请输入用法用量' }]">
          <a-input v-model:value="currentPrescription.usage" />
        </a-form-item>
        <a-form-item label="注意事项" :rules="[{ required: true, message: '请输入注意事项' }]">
          <a-input v-model:value="currentPrescription.precautions" />
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
const prescriptions = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增处方');
const isEdit = ref(false);
const currentPrescription = reactive({
  prescription_id: '',
  diagnosis_id: '',
  drug_id: '',
  drug_amount: '',
  usage: '',
  precautions: ''
});

const columns = [
  { title: '处方号', dataIndex: 'prescription_id', key: 'prescription_id' },
  { title: '诊断号', dataIndex: 'diagnosis_id', key: 'diagnosis_id' },
  { title: '药品号', dataIndex: 'drug_id', key: 'drug_id' },
  { title: '药品数量', dataIndex: 'drug_amount', key: 'drug_amount' },
  { title: '用法用量', dataIndex: 'usage', key: 'usage' },
  { title: '注意事项', dataIndex: 'precautions', key: 'precautions' },
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

function fetchPrescriptions() {
  http.request('/prescription/all', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    prescriptions.value = response.data;
  });
}

function showAddModal() {
  modalTitle.value = '新增处方';
  isEdit.value = false;
  Object.assign(currentPrescription, { prescription_id: '', diagnosis_id: '', drug_id: '', drug_amount: '', usage: '', precautions: '' });
  isModalVisible.value = true;
}

function handleEdit(record: any) {
  modalTitle.value = '编辑处方';
  isEdit.value = true;
  Object.assign(currentPrescription, record);
  isModalVisible.value = true;
}

async function handleOk() {
  if (isEdit.value) {
    try {
      await http.request('/prescription/update', 'POST_JSON', { ...currentPrescription });
      message.success('编辑处方信息成功');
    } finally {
      isModalVisible.value = false;
      fetchPrescriptions();
    }
  } else {
    try {
      await http.request('/prescription/add', 'POST_JSON', { ...currentPrescription });
      message.success('新增处方信息成功');
    } finally {
      isModalVisible.value = false;
      fetchPrescriptions();
    }
  }
}

function handleCancel() {
  isModalVisible.value = false;
}

function handleDelete(record: any) {
  http.request('/prescription/delete', 'POST_JSON', { prescription_id: record.prescription_id });
  message.success('删除处方信息成功');
  fetchPrescriptions();
}

onMounted(() => {
  fetchPrescriptions();
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