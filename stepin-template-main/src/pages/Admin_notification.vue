<template>
  <div class="admin-page">
    <h1 class="title">通知管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入通知号、通知内容或接收人学工号"
          @search="fetchNotifications"
          enter-button
          class="search-input"
      />
      <a-button type="primary" @click="showAddModal" class="add-button">
        <template #icon>
          <PlusOutlined />
        </template>
        新增通知
      </a-button>
    </div>
    <a-table v-bind="$attrs" :columns="columns" :dataSource="notifications" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'notification_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'notification_text'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'notification_time'" class="type3">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'staff_id'" class="type4">
          {{ text }}
        </div>
        <template v-else-if="column.dataIndex === 'edit'">
          <a-button type="link" @click="handleEdit(record)" class="edit-button">
            <EditOutlined />
            编辑
          </a-button>
        </template>
        <template v-else-if="column.dataIndex === 'delete'">
          <a-button type="link" @click="handleDelete(record.notification_id)" class="delete-button">
            <DeleteOutlined />
            删除
          </a-button>
        </template>
      </template>
    </a-table>
    <!-- 新增/编辑通知的模态框 -->
    <div v-if="isModalVisible" class="floating-modal" ref="modal">
      <div class="modal-header">
        <span>{{ modalTitle }}</span>
        <a-button type="link" @click="handleCancel">关闭</a-button>
      </div>
      <a-form :model="currentNotification" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }" ref="notificationForm" class="my-form">
        <a-form-item label="通知号" :rules="[{ required: true, message: '请输入通知号' }]">
          <a-input v-model:value="currentNotification.notification_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="通知内容" :rules="[{ required: true, message: '请输入通知内容' }]">
          <a-textarea v-model:value="currentNotification.notification_text" rows="3" />
        </a-form-item>
        <a-form-item label="通知时间" :rules="[{ required: true, message: '请输入通知时间' }]">
          <a-date-picker v-model:value="currentNotification.notification_time" format="YYYY-MM-DD HH:mm:ss" />
        </a-form-item>
        <a-form-item label="接收人学工号" :rules="[{ required: true, message: '请输入接收人学工号' }]">
          <a-input v-model:value="currentNotification.staff_id" />
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
const notifications = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增通知');
const isEdit = ref(false);
const currentNotification = reactive({
  notification_id: '',
  notification_text: '',
  notification_time: '',
  staff_id: ''
});

const columns = [
  { title: '通知号', dataIndex: 'notification_id', key: 'notification_id' },
  { title: '通知内容', dataIndex: 'notification_text', key: 'notification_text' },
  { title: '通知时间', dataIndex: 'notification_time', key: 'notification_time' },
  { title: '接收人学工号', dataIndex: 'staff_id', key: 'staff_id' },
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

function fetchNotifications() {
  http.request('/notification/all', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    notifications.value = response.data;
  });
}

function showAddModal() {
  modalTitle.value = '新增通知';
  isEdit.value = false;
  Object.assign(currentNotification, {
    notification_id: '',
    notification_text: '',
    notification_time: '',
    staff_id: ''
  });
  isModalVisible.value = true;
}

function handleEdit(record: any) {
  modalTitle.value = '编辑通知';
  isEdit.value = true;
  Object.assign(currentNotification, record);
  isModalVisible.value = true;
}

async function handleOk() {
  if (isEdit.value) {
    try {
      await http.request('/notification/update', 'POST_JSON', { ...currentNotification });
      message.success('编辑通知成功');
    } finally {
      isModalVisible.value = false;
      fetchNotifications();
    }
  } else {
    try {
      await http.request('/notification/add', 'POST_JSON', { ...currentNotification });
      message.success('新增通知成功');
    } finally {
      isModalVisible.value = false;
      fetchNotifications();
    }
  }
}

function handleCancel() {
  isModalVisible.value = false;
}

function handleDelete(notification_id: any) {
  http.request('/notification/delete', 'POST_JSON', { notification_id: notification_id });
  message.success('删除通知成功');
  fetchNotifications();
}

onMounted(() => {
  fetchNotifications();
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