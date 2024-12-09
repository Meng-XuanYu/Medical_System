<template>
  <div class="admin-page">
    <h1 class="title">药品库存管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入药品号、药房号"
          @search="fetchDrugStocks"
          enter-button
          class="search-input"
      />
      <a-button type="primary" @click="showAddModal" class="add-button">
        <template #icon>
          <PlusOutlined />
        </template>
        新增药品库存
      </a-button>
    </div>
    <a-table v-bind="$attrs" :columns="columns" :dataSource="drugStocks" :pagination="false" class="mytable">
      <template #bodyCell="{ column, text, record }">
        <div v-if="column.dataIndex === 'drug_id'" class="type1">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'drug_amount'" class="type2">
          {{ text }}
        </div>
        <div v-else-if="column.dataIndex === 'pharmacy_id'" class="type3">
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
      <a-form :model="currentDrugStock" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }" ref="drugStockForm" class="my-form">
        <a-form-item label="药品号" :rules="[{ required: true, message: '请输入药品号' }]">
          <a-input v-model:value="currentDrugStock.drug_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="药品数量" :rules="[{ required: true, message: '请输入药品数量' }]">
          <a-input-number v-model:value="currentDrugStock.drug_amount" />
        </a-form-item>
        <a-form-item label="药房号" :rules="[{ required: true, message: '请输入药房号' }]">
          <a-input v-model:value="currentDrugStock.pharmacy_id" />
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
const drugStocks = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增药品库存');
const isEdit = ref(false);
const currentDrugStock = reactive({
  drug_id: '',
  drug_amount: 0,
  pharmacy_id: ''
});

const columns = [
  { title: '药品号', dataIndex: 'drug_id', key: 'drug_id' },
  { title: '药品数量', dataIndex: 'drug_amount', key: 'drug_amount' },
  { title: '药房号', dataIndex: 'pharmacy_id', key: 'pharmacy_id' },
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

function fetchDrugStocks() {
  http.request('/drugstock/all/', 'POST_JSON', { searchText: searchText.value }).then((response) => {
    drugStocks.value = response.data;
  });
}

function showAddModal() {
  modalTitle.value = '新增药品库存';
  isEdit.value = false;
  Object.assign(currentDrugStock, { drug_id: '', drug_amount: 0, pharmacy_id: '' });
  isModalVisible.value = true;
}

function handleEdit(record: any) {
  modalTitle.value = '编辑药品库存';
  isEdit.value = true;
  Object.assign(currentDrugStock, record);
  isModalVisible.value = true;
}

async function handleOk() {
  if (isEdit.value) {
    try {
      await http.request('/drugstock/update/', 'POST_JSON', { ...currentDrugStock });
      message.success('编辑药品库存成功');
    } finally {
      isModalVisible.value = false;
      fetchDrugStocks();
    }
  } else {
    try {
      await http.request('/drugstock/add/', 'POST_JSON', { ...currentDrugStock });
      message.success('新增药品库存成功');
    } finally {
      isModalVisible.value = false;
      fetchDrugStocks();
    }
  }
}

function handleCancel() {
  isModalVisible.value = false;
}

async function handleDelete(record: any) {
  await http.request('/drugstock/delete/', 'POST_JSON', { drug_id: record.drug_id, pharmacy_id: record.pharmacy_id });
  message.success('删除药品库存成功');
  fetchDrugStocks();
}

onMounted(() => {
  fetchDrugStocks();
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