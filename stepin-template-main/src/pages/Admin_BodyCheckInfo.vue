<template>
  <div class="admin-page">
    <h1 class="title">体检信息管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入体检预约号、体检项目号、体检结果或体检学生的学号"
          @search="fetchExaminationInfos"
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
    <a-table v-bind="$attrs" :columns="columns" :dataSource="examinationInfos" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'exam_appointment_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'examination_id'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'examination_result'" class="type3">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'user_id'" class="type4">
          {{ text }}
        </div>
        <template v-else-if="column.dataIndex === 'edit'">
          <a-button type="link" @click="handleEdit(record)" class="edit-button">
            <EditOutlined />
            编辑
          </a-button>
        </template>
        <template v-else-if="column.dataIndex === 'delete'">
          <a-button type="link" @click="handleDelete(record.exam_appointment_id)" class="delete-button">
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
      <a-form :model="currentExaminationInfo" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }" ref="examinationForm" class="my-form">
        <a-form-item label="体检预约号" :rules="[{ required: true, message: '请输入体检预约号' }]">
          <a-input v-model:value="currentExaminationInfo.exam_appointment_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="体检项目号" :rules="[{ required: true, message: '请输入体检项目号' }]">
          <a-textarea v-model:value="currentExaminationInfo.examination_id" rows="3" />
        </a-form-item>
        <a-form-item label="体检结果" :rules="[{ required: true, message: '请输入体检结果' }]">
          <a-textarea v-model:value="currentExaminationInfo.examination_result" rows="3" />
        </a-form-item>
        <a-form-item label="体检人学号" :rules="[{ required: true, message: '请输入体检人学号' }]">
          <a-input v-model:value="currentExaminationInfo.user_id" />
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
const examinationInfos = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增体检预约信息');
const isEdit = ref(false);
const dateform = reactive({
  year: '',
  month: '',
  day: '',
});
const currentExaminationInfo = reactive({
  exam_appointment_id: '',
  examination_id: '',
  examination_result: '',
  user_id: '',
});


const columns = [
  { title: '体检预约号', dataIndex: 'exam_appointment_id', key: 'exam_appointment_id' },
  { title: '体检项目号', dataIndex: 'examination_id', key: 'examination_id' },
  { title: '体检结果', dataIndex: 'examination_result', key: 'examination_result' },
  { title: '体检人学号', dataIndex: 'user_id', key: 'user_id' },
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

function fetchExaminationInfos() {
  http.request('/examinationInfo/all/', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    examinationInfos.value = response.data;
  });
}

function showAddModal() {
  modalTitle.value = '新增体检预约信息';
  isEdit.value = false;
  Object.assign(currentExaminationInfo, {
    exam_appointment_id: '',
    examination_id: '',
    examination_result: '',
    user_id: '',
  });
  dateform.year = '';
  dateform.month = '';
  dateform.day = '';
  isModalVisible.value = true;
}

function handleEdit(record: any) {

  modalTitle.value = '编辑体检预约信息';
  isEdit.value = true;
  Object.assign(currentExaminationInfo, record);
  isModalVisible.value = true;
}

async function handleOk() {

  if (isEdit.value) {
    try {
      await http.request('/examinationInfo/update/', 'POST_JSON', { ...currentExaminationInfo });
      message.success('编辑体检预约信息成功');
    } finally {
      isModalVisible.value = false;
      fetchExaminationInfos();
    }
  } else {
    try {
      await http.request('/examinationInfo/add/', 'POST_JSON', { ...currentExaminationInfo });
      message.success('新增体检预约信息成功');
    } finally {
      isModalVisible.value = false;
      fetchExaminationInfos();
    }
  }
}

function handleCancel() {
  isModalVisible.value = false;
}

function handleDelete(examination_id: any) {
  http.request('/examinationInfo/delete/', 'POST_JSON', { examination_id: examination_id });
  message.success('删除体检预约信息成功');
  fetchExaminationInfos();
}

onMounted(() => {
  fetchExaminationInfos();
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