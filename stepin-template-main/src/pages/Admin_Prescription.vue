<template>
  <div>
    <h1>处方管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入处方号或诊断号"
          @search="fetchPrescriptions"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增处方</a-button>
    </div>
    <a-table :columns="columns" :data-source="prescriptions" row-key="prescription_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deletePrescription(record.prescription_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑处方信息的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
        width="800px"
    >
      <a-form
          :model="currentPrescription"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          ref="prescriptionForm"
      >
        <a-form-item label="处方号" :rules="[{ required: true, message: '请输入处方号' }]">
          <a-input v-model="currentPrescription.prescription_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="诊断号" :rules="[{ required: true, message: '请输入诊断号' }]">
          <a-input v-model="currentPrescription.diagnosis_id" />
        </a-form-item>
        <a-form-item label="药品号" :rules="[{ required: true, message: '请输入药品号' }]">
          <a-input v-model="currentPrescription.drug_id" />
        </a-form-item>
        <a-form-item label="药品数量" :rules="[{ required: true, message: '请输入药品数量' }]">
          <a-input-number v-model="currentPrescription.drug_amount" :min="1" />
        </a-form-item>
        <a-form-item label="用法用量" :rules="[{ required: true, message: '请输入用法用量' }]">
          <a-textarea v-model="currentPrescription.usage" rows="2" />
        </a-form-item>
        <a-form-item label="注意事项" :rules="[{ required: true, message: '请输入注意事项' }]">
          <a-textarea v-model="currentPrescription.precautions" rows="2" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const prescriptions = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增处方');
const isEdit = ref(false);
const currentPrescription = reactive({
  prescription_id: '',
  diagnosis_id: '',
  drug_id: '',
  drug_amount: 1,
  usage: '',
  precautions: '',
});

const columns = [
  { title: '处方号', dataIndex: 'prescription_id', key: 'prescription_id' },
  { title: '诊断号', dataIndex: 'diagnosis_id', key: 'diagnosis_id' },
  { title: '药品号', dataIndex: 'drug_id', key: 'drug_id' },
  { title: '药品数量', dataIndex: 'drug_amount', key: 'drug_amount' },
  { title: '用法用量', dataIndex: 'usage', key: 'usage' },
  { title: '注意事项', dataIndex: 'precautions', key: 'precautions' },
  {
    title: '操作',
    key: 'action',
    fixed: 'right',
    width: 120,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchPrescriptions() {
  // 调用后端API获取处方信息，支持搜索
  prescriptions.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增处方';
  isEdit.value = false;
  Object.assign(currentPrescription, {
    prescription_id: '',
    diagnosis_id: '',
    drug_id: '',
    drug_amount: 1,
    usage: '',
    precautions: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑处方';
  isEdit.value = true;
  Object.assign(currentPrescription, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.prescriptionForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新处方信息
      message.success('更新处方信息成功');
    } else {
      // 调用后端API新增处方
      message.success('新增处方成功');
    }
    isModalVisible.value = false;
    fetchPrescriptions();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deletePrescription(prescription_id) {
  // 调用后端API删除处方信息
  message.success('删除处方信息成功');
  fetchPrescriptions();
}

onMounted(() => {
  fetchPrescriptions();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
