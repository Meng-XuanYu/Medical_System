<template>
  <div class="admin-page">
    <h1 class="title">体检安排管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入体检号、体检项目、体检日期或负责医生的工号"
          @search="fetchExaminations"
          enter-button
          class="search-input"
      />
      <a-button type="primary" @click="showAddModal" class="add-button">
        <template #icon>
          <PlusOutlined />
        </template>
        新增体检项目
      </a-button>
    </div>
    <a-table v-bind="$attrs" :columns="columns" :dataSource="examinations" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'examination_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'examination'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'examination_date'" class="type3">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'doctor_id'" class="type4">
          {{ text }}
        </div>
        <template v-else-if="column.dataIndex === 'edit'">
          <a-button type="link" @click="handleEdit(record)" class="edit-button">
            <EditOutlined />
            编辑
          </a-button>
        </template>
        <template v-else-if="column.dataIndex === 'delete'">
          <a-button type="link" @click="handleDelete(record.examination_id)" class="delete-button">
            <DeleteOutlined />
            删除
          </a-button>
        </template>
        <div v-else class="text-subtext">
          {{ text }}
        </div>
      </template>
    </a-table>
    <!-- 新增/编辑体检项目的模态框 -->

    <div v-if="isModalVisible" class="floating-modal" ref="modal">
      <div class="modal-header">
        <span>{{ modalTitle }}</span>
        <a-button type="link" @click="handleCancel">关闭</a-button>
      </div>
      <a-form :model="currentExamination" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }" ref="examinationForm" class="my-form">
        <a-form-item label="体检号" :rules="[{ required: true, message: '请输入体检号' }]">
          <a-input v-model:value="currentExamination.examination_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="体检项目" :rules="[{ required: true, message: '请输入体检项目' }]">
          <a-textarea v-model:value="currentExamination.examination" rows="3" />
        </a-form-item>
        <a-form-item label="体检日期" :rules="[{ required: true, message: '请选择体检日期' }]">
          <div class="date-select-container">
            <a-select v-model:value="dateform.year" placeholder="年" class="date-select" :get-popup-container="(triggerNode) => triggerNode.parentNode">
              <a-select-option v-for="year in years" :key="year" :value="year">{{ year }}</a-select-option>
            </a-select>
            <a-select v-model:value="dateform.month" placeholder="月" class="date-select" :get-popup-container="(triggerNode) => triggerNode.parentNode">
              <a-select-option v-for="month in months" :key="month" :value="month">{{ month }}</a-select-option>
            </a-select>
            <a-select v-model:value="dateform.day" placeholder="日" class="date-select" :get-popup-container="(triggerNode) => triggerNode.parentNode">
              <a-select-option v-for="day in days" :key="day" :value="day">{{ day }}</a-select-option>
            </a-select>
          </div>
        </a-form-item>
        <a-form-item label="负责医生工号" :rules="[{ required: true, message: '请输入负责医生工号' }]">
          <a-input v-model:value="currentExamination.doctor_id" />
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
const examinations = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增体检项目');
const isEdit = ref(false);
const dateform = reactive({
  year: '',
  month: '',
  day: '',
});
const currentExamination = reactive({
  examination_id: '',
  examination: '',
  examination_date: '',
  doctor_id: '',
});

const years = Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - 50 + i);
const months = Array.from({ length: 12 }, (_, i) => i + 1);
const days = Array.from({ length: 31 }, (_, i) => i + 1);

const columns = [
  { title: '体检号', dataIndex: 'examination_id', key: 'examination_id' },
  { title: '体检项目', dataIndex: 'examination', key: 'examination' },
  { title: '体检日期', dataIndex: 'examination_date', key: 'examination_date' },
  { title: '负责医生工号', dataIndex: 'doctor_id', key: 'doctor_id' },
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

function fetchExaminations() {
  http.request('/examination/all', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    examinations.value = response.data;

  });
}

function showAddModal() {
  modalTitle.value = '新增体检项目';
  isEdit.value = false;
  Object.assign(currentExamination, {
    examination_id: '',
    examination: '',
    examination_date: '',
    doctor_id: '',
  });
  dateform.year = '';
  dateform.month = '';
  dateform.day = '';
  isModalVisible.value = true;
}

function handleEdit(record: any) {
  currentExamination.examination_date = dateform.day + '-' + dateform.month + '-' + dateform.year;
  modalTitle.value = '编辑体检项目';
  isEdit.value = true;
  Object.assign(currentExamination, record);
  isModalVisible.value = true;
}

async function handleOk() {
  currentExamination.examination_date = dateform.year + '-' + dateform.month + '-' + dateform.day;
  if (isEdit.value) {
    try {
      await http.request('/examination/update', 'POST_JSON', { ...currentExamination });
      message.success('编辑体检项目成功');
    } finally {
      isModalVisible.value = false;
      fetchExaminations();
    }
  } else {
    try {
      await http.request('/examination/add', 'POST_JSON', { ...currentExamination });
      message.success('新增体检项目成功');
    } finally {
      isModalVisible.value = false;
      fetchExaminations();
    }
  }
}

function handleCancel() {
  isModalVisible.value = false;
}

function handleDelete(examination_id: any) {
  http.request('/examination/delete', 'POST_JSON', { examination_id: examination_id });
  message.success('删除体检项目成功');
  fetchExaminations();
}

onMounted(() => {
  fetchExaminations();
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