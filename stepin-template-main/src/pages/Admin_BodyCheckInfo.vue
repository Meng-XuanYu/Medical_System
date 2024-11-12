<template>
  <div>
    <h1>体检信息管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入体检预约号、学工号或体检号"
          @search="fetchExamInfos"
          enter-button
      />
    </div>
    <a-table :columns="columns" :data-source="examInfos" row-key="exam_appointment_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteExamInfo(record.exam_appointment_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑体检信息的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentExamInfo"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="examInfoForm"
      >
        <a-form-item label="体检预约号" :rules="[{ required: true, message: '请输入体检预约号' }]">
          <a-input v-model="currentExamInfo.exam_appointment_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="体检号" :rules="[{ required: true, message: '请输入体检号' }]">
          <a-input v-model="currentExamInfo.examination_id" />
        </a-form-item>
        <a-form-item label="学工号" :rules="[{ required: true, message: '请输入学工号' }]">
          <a-input v-model="currentExamInfo.id" />
        </a-form-item>
        <a-form-item label="体检结果">
          <a-textarea v-model="currentExamInfo.examination_result" rows="3" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const examInfos = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增体检信息');
const isEdit = ref(false);
const currentExamInfo = reactive({
  exam_appointment_id: '',
  examination_id: '',
  examination_result: '',
  id: '',
});

const columns = [
  { title: '体检预约号', dataIndex: 'exam_appointment_id', key: 'exam_appointment_id' },
  { title: '体检号', dataIndex: 'examination_id', key: 'examination_id' },
  { title: '学工号', dataIndex: 'id', key: 'id' },
  { title: '体检结果', dataIndex: 'examination_result', key: 'examination_result' },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
];

function fetchExamInfos() {
  // 调用后端API获取体检信息数据，支持搜索
  examInfos.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增体检信息';
  isEdit.value = false;
  Object.assign(currentExamInfo, {
    exam_appointment_id: '',
    examination_id: '',
    examination_result: '',
    id: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑体检信息';
  isEdit.value = true;
  Object.assign(currentExamInfo, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.examInfoForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新体检信息
      message.success('更新体检信息成功');
    } else {
      // 调用后端API新增体检信息
      message.success('新增体检信息成功');
    }
    isModalVisible.value = false;
    fetchExamInfos();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteExamInfo(exam_appointment_id) {
  // 调用后端API删除体检信息
  message.success('删除体检信息成功');
  fetchExamInfos();
}

onMounted(() => {
  fetchExamInfos();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}
</style>

