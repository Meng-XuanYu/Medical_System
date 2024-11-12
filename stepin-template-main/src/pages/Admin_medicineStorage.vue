<template>
  <div>
    <h1>药品库存管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入药品号或药房号"
          @search="fetchDrugStocks"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增库存记录</a-button>
    </div>
    <a-table :columns="columns" :data-source="drugStocks" row-key="key">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteDrugStock(record.drug_id, record.pharmacy_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑库存的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentDrugStock"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="drugStockForm"
      >
        <a-form-item label="药品号" :rules="[{ required: true, message: '请输入药品号' }]">
          <a-input v-model="currentDrugStock.drug_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="药房号" :rules="[{ required: true, message: '请输入药房号' }]">
          <a-input v-model="currentDrugStock.pharmacy_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="库存数量" :rules="[{ required: true, message: '请输入库存数量' }]">
          <a-input-number v-model="currentDrugStock.drug_amount" :min="0" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const drugStocks = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增库存记录');
const isEdit = ref(false);
const currentDrugStock = reactive({
  drug_id: '',
  pharmacy_id: '',
  drug_amount: 0,
});

const columns = [
  { title: '药品号', dataIndex: 'drug_id', key: 'drug_id' },
  { title: '药房号', dataIndex: 'pharmacy_id', key: 'pharmacy_id' },
  { title: '库存数量', dataIndex: 'drug_amount', key: 'drug_amount' },
  {
    title: '操作',
    key: 'action',
    width: 120,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchDrugStocks() {
  // 调用后端API获取药品库存信息，支持搜索
  drugStocks.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增库存记录';
  isEdit.value = false;
  Object.assign(currentDrugStock, {
    drug_id: '',
    pharmacy_id: '',
    drug_amount: 0,
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑库存记录';
  isEdit.value = true;
  Object.assign(currentDrugStock, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.drugStockForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新库存信息
      message.success('更新库存信息成功');
    } else {
      // 调用后端API新增库存记录
      message.success('新增库存记录成功');
    }
    isModalVisible.value = false;
    fetchDrugStocks();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteDrugStock(drug_id, pharmacy_id) {
  // 调用后端API删除库存记录
  message.success('删除库存记录成功');
  fetchDrugStocks();
}

onMounted(() => {
  fetchDrugStocks();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
