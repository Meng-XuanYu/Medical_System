<template>
  <div>
    <h1>药品管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入药品号或药品名称"
          @search="fetchDrugs"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增药品</a-button>
    </div>
    <a-table :columns="columns" :data-source="drugs" row-key="drug_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteDrug(record.drug_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑药品的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentDrug"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="drugForm"
      >
        <a-form-item label="药品号" :rules="[{ required: true, message: '请输入药品号' }]">
          <a-input v-model="currentDrug.drug_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="药品名称" :rules="[{ required: true, message: '请输入药品名称' }]">
          <a-input v-model="currentDrug.drug_name" />
        </a-form-item>
        <a-form-item label="价格" :rules="[{ required: true, message: '请输入价格' }]">
          <a-input-number v-model="currentDrug.price" :min="0" :step="0.01" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const drugs = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增药品');
const isEdit = ref(false);
const currentDrug = reactive({
  drug_id: '',
  drug_name: '',
  price: 0,
});

const columns = [
  { title: '药品号', dataIndex: 'drug_id', key: 'drug_id' },
  { title: '药品名称', dataIndex: 'drug_name', key: 'drug_name' },
  { title: '价格', dataIndex: 'price', key: 'price' },
  {
    title: '操作',
    key: 'action',
    width: 120,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchDrugs() {
  // 调用后端API获取药品信息，支持搜索
  drugs.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增药品';
  isEdit.value = false;
  Object.assign(currentDrug, {
    drug_id: '',
    drug_name: '',
    price: 0,
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑药品';
  isEdit.value = true;
  Object.assign(currentDrug, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.drugForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新药品信息
      message.success('更新药品信息成功');
    } else {
      // 调用后端API新增药品
      message.success('新增药品成功');
    }
    isModalVisible.value = false;
    fetchDrugs();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteDrug(drug_id) {
  // 调用后端API删除药品
  message.success('删除药品成功');
  fetchDrugs();
}

onMounted(() => {
  fetchDrugs();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
