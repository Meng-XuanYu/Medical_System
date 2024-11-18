<template>
  <div class="admin-page">
    <h1 class="title">预约管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入预约号、患者与预约人关系、排班号"
          @search="fetchAppointments"
          enter-button
          class="search-input"
      />
      <a-button type="primary" @click="showAddModal" class="add-button">
        <template #icon>
          <PlusOutlined />
        </template>
        新增预约
      </a-button>
    </div>
    <a-table v-bind="$attrs" :columns="columns" :dataSource="appointments" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'appointment_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'relationship'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'schedule_id'" class="type3">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'id'" class="type4">
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
      <a-form :model="currentAppointment" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }" ref="appointmentForm" class="my-form">
        <a-form-item label="预约号" :rules="[{ required: true, message: '请输入预约号' }]">
          <a-input v-model:value="currentAppointment.appointment_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="患者与预约人关系" :rules="[{ required: true, message: '请输入患者与预约人关系' }]">
          <a-input v-model:value="currentAppointment.relationship" />
        </a-form-item>
        <a-form-item label="排班号" :rules="[{ required: true, message: '请输入排班号' }]">
          <a-input v-model:value="currentAppointment.schedule_id" />
        </a-form-item>
        <a-form-item label="学工号" :rules="[{ required: true, message: '请输入学工号' }]">
          <a-input v-model:value="currentAppointment.id" />
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
const appointments = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增预约');
const isEdit = ref(false);
const currentAppointment = reactive({
  appointment_id: '',
  relationship: '',
  schedule_id: '',
  id: ''
});

const columns = [
  { title: '预约号', dataIndex: 'appointment_id', key: 'appointment_id' },
  { title: '患者与预约人关系', dataIndex: 'relationship', key: 'relationship' },
  { title: '排班号', dataIndex: 'schedule_id', key: 'schedule_id' },
  { title: '学工号', dataIndex: 'id', key: 'id' },
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

function fetchAppointments() {
  http.request('/appointment/all', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    appointments.value = response.data;
  });
}

function showAddModal() {
  modalTitle.value = '新增预约';
  isEdit.value = false;
  Object.assign(currentAppointment, { appointment_id: '', relationship: '', schedule_id: '', id: '' });
  isModalVisible.value = true;
}

function handleEdit(record: any) {
  modalTitle.value = '编辑预约';
  isEdit.value = true;
  Object.assign(currentAppointment, record);
  isModalVisible.value = true;
}

async function handleOk() {
  if (isEdit.value) {
    try {
      await http.request('/appointment/update', 'POST_JSON', { ...currentAppointment });
      message.success('编辑预约信息成功');
    } finally {
      isModalVisible.value = false;
      fetchAppointments();
    }
  } else {
    try {
      await http.request('/appointment/add', 'POST_JSON', { ...currentAppointment });
      message.success('新增预约信息成功');
    } finally {
      isModalVisible.value = false;
      fetchAppointments();
    }
  }
}

function handleCancel() {
  isModalVisible.value = false;
}

function handleDelete(record: any) {
  http.request('/appointment/delete', 'POST_JSON', { appointment_id: record.appointment_id });
  message.success('删除预约信息成功');
  fetchAppointments();
}

onMounted(() => {
  fetchAppointments();
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