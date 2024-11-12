<template>
  <div>
    <h1>科室管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入科室号或科室名称"
          @search="fetchDepartments"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增科室</a-button>
    </div>
    <a-table :columns="columns" :data-source="departments" row-key="department_id">
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteDepartment(record.department_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑科室的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentDepartment"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="departmentForm"
      >
        <a-form-item label="科室号" :rules="[{ required: true, message: '请输入科室号' }]">
          <a-input v-model="currentDepartment.department_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="科室名称" :rules="[{ required: true, message: '请输入科室名称' }]">
          <a-input v-model="currentDepartment.department_name" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const departments = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增科室');
const isEdit = ref(false);
const currentDepartment = reactive({
  department_id: '',
  department_name: '',
});

const columns = [
  { title: '科室号', dataIndex: 'department_id', key: 'department_id' },
  { title: '科室名称', dataIndex: 'department_name', key: 'department_name' },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
];

function fetchDepartments() {
  // 调用后端API获取科室信息，支持搜索
  departments.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增科室';
  isEdit.value = false;
  Object.assign(currentDepartment, {
    department_id: '',
    department_name: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑科室';
  isEdit.value = true;
  Object.assign(currentDepartment, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.departmentForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新科室信息
      message.success('更新科室信息成功');
    } else {
      // 调用后端API新增科室
      message.success('新增科室成功');
    }
    isModalVisible.value = false;
    fetchDepartments();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteDepartment(department_id) {
  // 调用后端API删除科室
  message.success('删除科室成功');
  fetchDepartments();
}

onMounted(() => {
  fetchDepartments();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
