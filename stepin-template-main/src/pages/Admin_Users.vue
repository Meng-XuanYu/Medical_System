<template>
  <div>
    <h1>用户管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入学工号、姓名或手机号"
          @search="fetchUsers"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增用户</a-button>
    </div>
    <a-table :columns="columns" :data-source="users" row-key="id">
      <template #gender="{ text }">
        <span>{{ text === 'M' ? '男' : '女' }}</span>
      </template>
      <template #user_type="{ text }">
        <span>{{ getUserTypeText(text) }}</span>
      </template>
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteUser(record.id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑用户的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentUser"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="userForm"
      >
        <a-form-item label="学工号" :rules="[{ required: true, message: '请输入学工号' }]">
          <a-input v-model="currentUser.id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="密码" :rules="[{ required: true, message: '请输入密码' }]">
          <a-input v-model="currentUser.password" type="password" />
        </a-form-item>
        <a-form-item label="姓名" :rules="[{ required: true, message: '请输入姓名' }]">
          <a-input v-model="currentUser.name" />
        </a-form-item>
        <a-form-item label="性别" :rules="[{ required: true, message: '请选择性别' }]">
          <a-select v-model="currentUser.gender">
            <a-select-option value="M">男</a-select-option>
            <a-select-option value="F">女</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="出生日期" :rules="[{ required: true, message: '请选择出生日期' }]">
          <a-date-picker v-model="currentUser.birth" format="YYYY-MM-DD" />
        </a-form-item>
        <a-form-item label="身份证号" :rules="[{ required: true, message: '请输入身份证号' }]">
          <a-input v-model="currentUser.id_number" />
        </a-form-item>
        <a-form-item label="用户类型" :rules="[{ required: true, message: '请选择用户类型' }]">
          <a-select v-model="currentUser.user_type">
            <a-select-option value="S">学生</a-select-option>
            <a-select-option value="T">教师</a-select-option>
            <a-select-option value="O">其他</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="手机号" :rules="[{ required: true, message: '请输入手机号' }]">
          <a-input v-model="currentUser.phone" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const users = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增用户');
const isEdit = ref(false);
const currentUser = reactive({
  id: '',
  password: '',
  name: '',
  gender: '',
  birth: null,
  id_number: '',
  user_type: '',
  phone: '',
});

const columns = [
  { title: '学工号', dataIndex: 'id', key: 'id' },
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '性别', dataIndex: 'gender', key: 'gender', scopedSlots: { customRender: 'gender' } },
  { title: '出生日期', dataIndex: 'birth', key: 'birth' },
  { title: '身份证号', dataIndex: 'id_number', key: 'id_number' },
  { title: '用户类型', dataIndex: 'user_type', key: 'user_type', scopedSlots: { customRender: 'user_type' } },
  { title: '手机号', dataIndex: 'phone', key: 'phone' },
  {
    title: '操作',
    key: 'action',
    width: 120,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchUsers() {
  // 调用后端API获取用户信息，支持搜索
  users.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增用户';
  isEdit.value = false;
  Object.assign(currentUser, {
    id: '',
    password: '',
    name: '',
    gender: '',
    birth: null,
    id_number: '',
    user_type: '',
    phone: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑用户';
  isEdit.value = true;
  Object.assign(currentUser, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.userForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新用户信息
      message.success('更新用户信息成功');
    } else {
      // 调用后端API新增用户
      message.success('新增用户成功');
    }
    isModalVisible.value = false;
    fetchUsers();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteUser(id) {
  // 调用后端API删除用户
  message.success('删除用户成功');
  fetchUsers();
}

function getUserTypeText(type) {
  switch (type) {
    case 'S':
      return '学生';
    case 'T':
      return '教师';
    default:
      return '其他';
  }
}

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
