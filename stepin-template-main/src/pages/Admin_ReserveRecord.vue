<template>
  <div>
    <h1>预约信息管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入预约号、学工号或排班号"
          @search="fetchAppointments"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增预约</a-button>
    </div>
    <a-table :columns="columns" :data-source="appointments" row-key="appointment_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteAppointment(record.appointment_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑预约信息的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentAppointment"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="appointmentForm"
      >
        <a-form-item label="预约号" :rules="[{ required: true, message: '请输入预约号' }]">
          <a-input v-model="currentAppointment.appointment_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="患者关系" :rules="[{ required: true, message: '请输入患者关系' }]">
          <a-input v-model="currentAppointment.relationship" />
        </a-form-item>
        <a-form-item label="排班号" :rules="[{ required: true, message: '请输入排班号' }]">
          <a-input v-model="currentAppointment.schedule_id" />
        </a-form-item>
        <a-form-item label="学工号" :rules="[{ required: true, message: '请输入学工号' }]">
          <a-input v-model="currentAppointment.id" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const appointments = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增预约');
const isEdit = ref(false);
const currentAppointment = reactive({
  appointment_id: '',
  relationship: '',
  schedule_id: '',
  id: '',
});

const columns = [
  { title: '预约号', dataIndex: 'appointment_id', key: 'appointment_id' },
  { title: '患者关系', dataIndex: 'relationship', key: 'relationship' },
  { title: '排班号', dataIndex: 'schedule_id', key: 'schedule_id' },
  { title: '学工号', dataIndex: 'id', key: 'id' },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
];

function fetchAppointments() {
  // 调用后端API获取预约信息，支持搜索
  appointments.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增预约';
  isEdit.value = false;
  Object.assign(currentAppointment, {
    appointment_id: '',
    relationship: '',
    schedule_id: '',
    id: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑预约';
  isEdit.value = true;
  Object.assign(currentAppointment, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.appointmentForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新预约信息
      message.success('更新预约信息成功');
    } else {
      // 调用后端API新增预约
      message.success('新增预约成功');
    }
    isModalVisible.value = false;
    fetchAppointments();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteAppointment(appointment_id) {
  // 调用后端API删除预约
  message.success('删除预约成功');
  fetchAppointments();
}

onMounted(() => {
  fetchAppointments();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
