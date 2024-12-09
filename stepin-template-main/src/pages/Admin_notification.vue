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
    <a-table
        :columns="columns"
        :dataSource="notifications"
        :pagination="false"
        class="mytable"
        rowKey="notification_id"
    >
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'notification_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'notification'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'notification_time'" class="type3">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'user'" class="type4">
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
    <!-- 新增通知的模态框 -->
    <div class="floating-modal" ref="modal"
        v-if="isAddModalVisible"
        title="新增通知"

    >
      <a-form :model="newNotification" ref="notificationForm" class="myForm">
        <a-form-item label="通知内容" :rules="[{ required: true, message: '请输入通知内容' }]">
          <a-textarea v-model:value="newNotification.content" rows="4" placeholder="请输入通知内容" />
        </a-form-item>
        <a-form-item label="选择接收用户">
          <div class="user-selection">
            <a-row :gutter="[16, 16]">
              <a-col
                  v-for="user in allUsers"
                  :key="user.user_id || user.doctor_id"
                  :span="6"
              >

                <a-card >

                  <img :src="user.image_url" width="50px">

                  <a-checkbox
                      v-model:checked="selectedUserIds"
                      :value="user.is_doctor ? `doctor_${user.doctor_id}` : `user_${user.user_id}`"
                  >
                    <div class="user-info">
                      <p class="user-name">{{ user.name }}</p>
                      <p v-if="user.title" class="user-title">{{ user.title }}</p>
                    </div>
                  </a-checkbox>
                </a-card>
              </a-col>
            </a-row>
          </div>
        </a-form-item>

      </a-form>
      <div>

          <a-button key="back" @click="handleCancel">取消</a-button>
          <a-button key="submit" type="primary" @click="handleSendNotifications">发送通知</a-button>

      </div>
    </div>
    <!-- 编辑通知的模态框 -->
    <a-modal
        v-model:visible="isEditModalVisible"
        title="编辑通知"
        @ok="handleUpdateNotification"

        ok-text="确认"
        cancel-text="取消"
        width="600px"
    >
      <a-form :model="currentNotification" layout="vertical" ref="editNotificationForm">
        <a-form-item label="通知内容" :rules="[{ required: true, message: '请输入通知内容' }]">
          <a-textarea v-model:value="currentNotification.notification" rows="4" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="tsx">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import http from "@/store/http";

// 搜索文本
const searchText = ref('');

// 通知列表
const notifications = ref([]);

// 新增通知模态框可见性
const isAddModalVisible = ref(false);

// 编辑通知模态框可见性
const isEditModalVisible = ref(false);

// 当前编辑的通知
const currentNotification = reactive({
  notification_id: '',
  notification: '',
});

// 新增通知数据
const newNotification = reactive({
  content: '',
});

// 所有用户和医生
const allUsers = ref([]);

// 选中的用户ID数组
const selectedUserIds = ref([]);

// 表格列定义
const columns = [
  { title: '通知号', dataIndex: 'notification_id', key: 'notification_id' },
  { title: '通知内容', dataIndex: 'notification', key: 'notification' },
  { title: '通知时间', dataIndex: 'notification_time', key: 'notification_time' },
  { title: '接收人学工号', dataIndex: 'user', key: 'user' },
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

// 获取通知列表
function fetchNotifications() {
  http.request('/notification/all/', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    notifications.value = response.data;
  }).catch((error) => {
    console.error('获取通知失败:', error);
    message.error('获取通知失败，请稍后再试。');
  });
}
async function getImage(image: string) {
  try {
    const response = await http.request('getImageUrl/', 'GET', { image: image });
    console.log(response.data.data as string);
    return response.data.data as string;
  } catch (error) {
    console.error('Error fetching image:', error);
    throw error;  // 或者根据需要处理错误
  }
}
// 获取所有用户和医生
async function fetchAllUsers() {
  try {
    const response = await http.request('/user/all/', 'POST_JSON');
    const users = response.data;

    const usersWithImages = await Promise.all(users.map(async user => {
      const imageUrl = await getImage(user.image);
      return {
        ...user,
        image_url: imageUrl,
        is_doctor: !!user.doctor_id,
      };
    }));

    allUsers.value = usersWithImages;
    console.log(allUsers.value);
  } catch (error) {
    console.error('Error fetching users:', error);
    message.error('获取用户信息失败，请稍后再试。');
  }
}

// 显示新增通知模态框
function showAddModal() {
  newNotification.content = '';
  selectedUserIds.value = [];
  isAddModalVisible.value = true;
}

// 处理取消新增或编辑
function handleCancel() {
  isAddModalVisible.value = false;
  isEditModalVisible.value = false;
}

// 处理编辑通知
function handleEdit(record: any) {
  currentNotification.notification_id = record.notification_id;
  currentNotification.notification = record.notification;
  isEditModalVisible.value = true;
}

// 处理删除通知
async function handleDelete(notification_id: any) {
  try {
    await http.request('/notification/delete/', 'POST_JSON', { notification_id: notification_id });
    message.success('删除通知成功');
    fetchNotifications();
  } catch (error) {
    console.error('删除通知失败:', error);
    message.error('删除通知失败，请稍后再试。');
  }
}

// 发送通知给选中的用户
async function handleSendNotifications() {
  if (!newNotification.content.trim()) {
    message.error('通知内容不能为空。');
    return;
  }
  if (selectedUserIds.value.length === 0) {
    message.error('请至少选择一个接收用户。');
    return;
  }

  // 遍历选中的用户ID，发送通知
  for (const userId of selectedUserIds.value) {
    const [type, id] = userId.split('_'); // 'user_1' 或 'doctor_2'
    const payload = {
      content: newNotification.content,
      user_id: id,
      user_type: type, // 可能需要后端区分是用户还是医生
    };
    try {
      await http.request('/notification/send/', 'POST_JSON', payload);
      message.success(`通知已发送给 ${type === 'user' ? '用户' : '医生'} ID: ${id}`);
    } catch (error) {
      console.error(`发送通知给 ${type === 'user' ? '用户' : '医生'} ID: ${id} 失败:`, error);
      message.error(`发送通知给 ${type === 'user' ? '用户' : '医生'} ID: ${id} 失败。`);
    }
  }

  isAddModalVisible.value = false;
  fetchNotifications();
}

// 更新通知
async function handleUpdateNotification() {
  if (!currentNotification.notification.trim()) {
    message.error('通知内容不能为空。');
    return;
  }
  try {
    await http.request('/notification/update/', 'POST_JSON', {
      notification_id: currentNotification.notification_id,
      notification: currentNotification.notification,
    });
    message.success('编辑通知成功');
    isEditModalVisible.value = false;
    fetchNotifications();
  } catch (error) {
    console.error('编辑通知失败:', error);
    message.error('编辑通知失败，请稍后再试。');
  }
}

onMounted(async () => {
  fetchNotifications();
  await fetchAllUsers();
});
</script>

<style scoped>
.admin-page {
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
  font-family: 'Arial', sans-serif;
}
.myForm {
  display: flex;
  flex-direction: column;
  gap: 30px;
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

.user-selection {
  gap: 30px;
  min-height: 400px;
  overflow-y: visible;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.floating-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 600px;
  min-height: 600px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 999;
  padding: 20px;
  overflow: hidden;
  cursor: move;
}
.user-name {
  font-weight: bold;
  margin: 8px 0 4px 0;
}

.user-title {
  font-size: 0.9em;
  color: #666;
}

@media (max-width: 768px) {
  .search-input {
    width: 100%;
  }
}
</style>
