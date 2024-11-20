<template>
  <div class="admin-page">
    <h1 class="title">家属管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入家属号、姓名"
          @search="fetchFamilyMembers"
          enter-button
          class="search-input"
      />
      <a-button type="primary" @click="showAddModal" class="add-button">
        <template #icon>
          <PlusOutlined />
        </template>
        新增家属信息
      </a-button>
    </div>
    <a-table v-bind="$attrs" :columns="columns" :dataSource="familyMembers" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'family_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'name'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'relationship'" class="type3">
          {{ text }}
        </div>
        <template v-else-if="column.dataIndex === 'edit'">
          <a-button type="link" @click="handleEdit(record)" class="edit-button">
            <EditOutlined />
            编辑
          </a-button>
        </template>
        <template v-else-if="column.dataIndex === 'delete'">
          <a-button type="link" @click="handleDelete(record.family_id)" class="delete-button">
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
      <a-form :model="currentFamilyMember" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }" ref="familyForm" class="my-form">
        <a-form-item label="家属号" :rules="[{ required: true, message: '请输入家属号' }]">
          <a-input v-model:value="currentFamilyMember.family_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="姓名" :rules="[{ required: true, message: '请输入姓名' }]">
          <a-input v-model:value="currentFamilyMember.name" />
        </a-form-item>
        <a-form-item label="关系" :rules="[{ required: true, message: '请输入关系' }]">
          <a-input v-model:value="currentFamilyMember.relationship" />
        </a-form-item>
        <a-form-item label="性别" :rules="[{ required: true, message: '请输入性别' }]">
          <a-select v-model:value="currentFamilyMember.gender" placeholder="选择性别">
            <a-select-option value="M">男</a-select-option>
            <a-select-option value="F">女</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="出生日期" :rules="[{ required: true, message: '请输入出生日期' }]">
          <a-date-picker v-model:value="currentFamilyMember.birth" />
        </a-form-item>
        <a-form-item label="身份证号" :rules="[{ required: true, message: '请输入身份证号' }]">
          <a-input v-model:value="currentFamilyMember.id_number" />
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
const familyMembers = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增家属信息');
const isEdit = ref(false);
const currentFamilyMember = reactive({
  family_id: '',
  name: '',
  relationship: '',
  gender: '',
  birth: '',
  id_number: ''
});

const columns = [
  { title: '家属号', dataIndex: 'family_id', key: 'family_id' },
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '关系', dataIndex: 'relationship', key: 'relationship' },
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

function fetchFamilyMembers() {
  http.request('/family/all/', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    familyMembers.value = response.data;
  });
}

function showAddModal() {
  modalTitle.value = '新增家属信息';
  isEdit.value = false;
  Object.assign(currentFamilyMember, {
    family_id: '',
    name: '',
    relationship: '',
    gender: '',
    birth: '',
    id_number: ''
  });
  isModalVisible.value = true;
}

function handleEdit(record: any) {
  modalTitle.value = '编辑家属信息';
  isEdit.value = true;
  Object.assign(currentFamilyMember, record);
  isModalVisible.value = true;
}

async function handleOk() {
  if (isEdit.value) {
    try {
      await http.request('/family/update/', 'POST_JSON', { ...currentFamilyMember });
      message.success('编辑家属信息成功');
    } finally {
      isModalVisible.value = false;
      fetchFamilyMembers();
    }
  } else {
    try {
      await http.request('/family/add/', 'POST_JSON', { ...currentFamilyMember });
      message.success('新增家属信息成功');
    } finally {
      isModalVisible.value = false;
      fetchFamilyMembers();
    }
  }
}

function handleCancel() {
  isModalVisible.value = false;
}

function handleDelete(family_id: any) {
  http.request('/family/delete/', 'POST_JSON', { family_id });
  message.success('删除家属信息成功');
  fetchFamilyMembers();
}

onMounted(() => {
  fetchFamilyMembers();
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