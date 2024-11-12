<template>
  <div>
    <h1>体检安排管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入体检号或体检项目"
          @search="fetchExaminations"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增体检项目</a-button>
    </div>
    <a-table :columns="columns" :data-source="examinations" row-key="examination_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteExamination(record.examination_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑体检项目的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentExamination"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="examinationForm"
      >
        <a-form-item label="体检号" :rules="[{ required: true, message: '请输入体检号' }]">
          <a-input v-model="currentExamination.examination_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="体检项目" :rules="[{ required: true, message: '请输入体检项目' }]">
          <a-textarea v-model="currentExamination.examination" rows="3" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const examinations = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增体检项目');
const isEdit = ref(false);
const currentExamination = reactive({
  examination_id: '',
  examination: '',
});

const columns = [
  { title: '体检号', dataIndex: 'examination_id', key: 'examination_id' },
  { title: '体检项目', dataIndex: 'examination', key: 'examination' },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
];

function fetchExaminations() {
  // 调用后端API获取体检安排，支持搜索
  examinations.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增体检项目';
  isEdit.value = false;
  Object.assign(currentExamination, {
    examination_id: '',
    examination: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑体检项目';
  isEdit.value = true;
  Object.assign(currentExamination, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.examinationForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新体检项目
      message.success('更新体检项目成功');
    } else {
      // 调用后端API新增体检项目
      message.success('新增体检项目成功');
    }
    isModalVisible.value = false;
    fetchExaminations();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteExamination(examination_id) {
  // 调用后端API删除体检项目
  message.success('删除体检项目成功');
  fetchExaminations();
}

onMounted(() => {
  fetchExaminations();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
