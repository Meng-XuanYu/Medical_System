<template>
  <div class="admin-page">
    <h1 class="title">用户管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入学工号、姓名、手机号"
          @search="fetchUsers"
          enter-button
          class="search-input"
      />
    </div>
    <a-table v-bind="$attrs" :columns="columns" :dataSource="users" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'user_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'name'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'phone'" class="type3">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'user_type'" class="type4">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'user_image'" class="type5">
          <img :src="text" width="50px" height="50px" />
        </div>
        <template v-else-if="column.dataIndex === 'delete'">
          <a-button type="link" @click="handleDelete(record.user_id)" class="delete-button">
            <DeleteOutlined />
            删除
          </a-button>
        </template>
        <div v-else class="text-subtext">
          {{ text }}
        </div>
      </template>
    </a-table>


  </div>
</template>

<script setup lang="tsx">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import http from "@/store/http";

const searchText = ref('');
const users = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增用户');
const isEdit = ref(false);
const currentUser = reactive({
  user_id: '',
  name: '',
  phone: '',
  user_type: '',
  user_image: '',
});

const columns = [
  { title: '学工号', dataIndex: 'user_id', key: 'user_id' },
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '手机号', dataIndex: 'phone', key: 'phone' },
  { title: '用户类型', dataIndex: 'user_type', key: 'user_type' },
  { title: '用户头像', dataIndex: 'user_image', key: 'user_image' },
  {
    title: '操作',
    dataIndex: 'delete',
    key: 'delete',
    width: 100,
  }
];
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
async function fetchUsers() {
  http.request('/user/all/', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    users.value = response.data;
    users.value.forEach(async (user: any) => {
      user.user_image = await getImage(user.image);
    });
  });
}

function showAddModal() {
  modalTitle.value = '新增用户';
  isEdit.value = false;
  Object.assign(currentUser, { user_id: '', name: '', phone: '', user_type: '', user_image: '' });
  isModalVisible.value = true;
}





function handleCancel() {
  isModalVisible.value = false;
}

async function handleDelete(id: any) {
  await http.request('/user/delete/', 'POST_JSON', { 'user_id': id });
  message.success('删除用户信息成功');
  fetchUsers();
}

onMounted(() => {
  fetchUsers();
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