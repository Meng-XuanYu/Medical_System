<template>
  <div>
    <h1>医生排班管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入排班号、医工号或医生姓名"
          @search="fetchSchedules"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增排班</a-button>
    </div>
    <a-table :columns="columns" :data-source="schedules" row-key="schedule_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteSchedule(record.schedule_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑排班的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentSchedule"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="scheduleForm"
      >
        <a-form-item label="排班号" :rules="[{ required: true, message: '请输入排班号' }]">
          <a-input v-model="currentSchedule.schedule_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="医工号" :rules="[{ required: true, message: '请输入医工号' }]">
          <a-input v-model="currentSchedule.staff_id" />
        </a-form-item>
        <a-form-item label="科室号" :rules="[{ required: true, message: '请输入科室号' }]">
          <a-input v-model="currentSchedule.department_id" />
        </a-form-item>
        <a-form-item label="排班时间" :rules="[{ required: true, message: '请选择排班时间' }]">
          <a-date-picker
              v-model="currentSchedule.schedule_time"
              show-time
              format="YYYY-MM-DD HH:mm:ss"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const schedules = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增排班');
const isEdit = ref(false);
const currentSchedule = reactive({
  schedule_id: '',
  staff_id: '',
  department_id: '',
  schedule_time: null,
});

const columns = [
  { title: '排班号', dataIndex: 'schedule_id', key: 'schedule_id' },
  { title: '医工号', dataIndex: 'staff_id', key: 'staff_id' },
  { title: '科室号', dataIndex: 'department_id', key: 'department_id' },
  { title: '排班时间', dataIndex: 'schedule_time', key: 'schedule_time' },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
];

function fetchSchedules() {
  // 调用后端API获取排班信息，支持搜索
  schedules.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增排班';
  isEdit.value = false;
  Object.assign(currentSchedule, {
    schedule_id: '',
    staff_id: '',
    department_id: '',
    schedule_time: null,
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑排班';
  isEdit.value = true;
  Object.assign(currentSchedule, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.scheduleForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新排班信息
      message.success('更新排班信息成功');
    } else {
      // 调用后端API新增排班
      message.success('新增排班成功');
    }
    isModalVisible.value = false;
    fetchSchedules();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteSchedule(schedule_id) {
  // 调用后端API删除排班
  message.success('删除排班成功');
  fetchSchedules();
}

onMounted(() => {
  fetchSchedules();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
