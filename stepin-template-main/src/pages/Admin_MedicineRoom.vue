<template>
  <div>
    <h1>药房管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入药房号或药房名称"
          @search="fetchPharmacies"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增药房</a-button>
    </div>
    <a-table :columns="columns" :data-source="pharmacies" row-key="pharmacy_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deletePharmacy(record.pharmacy_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑药房的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentPharmacy"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="pharmacyForm"
      >
        <a-form-item label="药房号" :rules="[{ required: true, message: '请输入药房号' }]">
          <a-input v-model="currentPharmacy.pharmacy_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="药房名称" :rules="[{ required: true, message: '请输入药房名称' }]">
          <a-input v-model="currentPharmacy.pharmacy_name" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const pharmacies = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增药房');
const isEdit = ref(false);
const currentPharmacy = reactive({
  pharmacy_id: '',
  pharmacy_name: '',
});

const columns = [
  { title: '药房号', dataIndex: 'pharmacy_id', key: 'pharmacy_id' },
  { title: '药房名称', dataIndex: 'pharmacy_name', key: 'pharmacy_name' },
  {
    title: '操作',
    key: 'action',
    width: 120,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchPharmacies() {
  // 调用后端API获取药房信息，支持搜索
  pharmacies.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增药房';
  isEdit.value = false;
  Object.assign(currentPharmacy, {
    pharmacy_id: '',
    pharmacy_name: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑药房';
  isEdit.value = true;
  Object.assign(currentPharmacy, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.pharmacyForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新药房信息
      message.success('更新药房信息成功');
    } else {
      // 调用后端API新增药房
      message.success('新增药房成功');
    }
    isModalVisible.value = false;
    fetchPharmacies();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deletePharmacy(pharmacy_id) {
  // 调用后端API删除药房
  message.success('删除药房成功');
  fetchPharmacies();
}

onMounted(() => {
  fetchPharmacies();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
