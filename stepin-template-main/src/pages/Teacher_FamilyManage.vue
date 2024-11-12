<!-- FamilyManagement.vue -->
<template>
  <div class="family-management-page">
    <h1>家属管理</h1>
    <div class="action-bar">
      <a-button type="primary" @click="showAddModal">新增家属</a-button>
    </div>
    <a-table :columns="columns" :data-source="familyMembers" :row-key="record => record.family_id">
      <template #gender="{ text }">
        <span>{{ text === 'M' ? '男' : '女' }}</span>
      </template>
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteFamilyMember(record.family_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑家属的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentFamilyMember"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="familyForm"
      >
        <a-form-item label="家属号" :rules="[{ required: true, message: '请输入家属号' }]">
          <a-input v-model="currentFamilyMember.family_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="关系" :rules="[{ required: true, message: '请输入关系' }]">
          <a-input v-model="currentFamilyMember.relationship" />
        </a-form-item>
        <a-form-item label="姓名" :rules="[{ required: true, message: '请输入姓名' }]">
          <a-input v-model="currentFamilyMember.name" />
        </a-form-item>
        <a-form-item label="性别" :rules="[{ required: true, message: '请选择性别' }]">
          <a-select v-model="currentFamilyMember.gender">
            <a-select-option value="M">男</a-select-option>
            <a-select-option value="F">女</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="出生日期" :rules="[{ required: true, message: '请选择出生日期' }]">
          <a-date-picker v-model="currentFamilyMember.birth" format="YYYY-MM-DD" />
        </a-form-item>
        <a-form-item label="身份证号" :rules="[{ required: true, message: '请输入身份证号' }]">
          <a-input v-model="currentFamilyMember.id_number" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';

const user = {
  id: 'T1234567',
  name: '李老师',
};

const familyMembers = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增家属');
const isEdit = ref(false);
const currentFamilyMember = reactive({
  family_id: '',
  id: user.id,
  relationship: '',
  name: '',
  gender: '',
  birth: null,
  id_number: '',
});

const columns = [
  { title: '家属号', dataIndex: 'family_id', key: 'family_id' },
  { title: '关系', dataIndex: 'relationship', key: 'relationship' },
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '性别', dataIndex: 'gender', key: 'gender', slots: { customRender: 'gender' } },
  { title: '出生日期', dataIndex: 'birth', key: 'birth' },
  { title: '身份证号', dataIndex: 'id_number', key: 'id_number' },
  {
    title: '操作',
    key: 'action',
    width: 120,
    slots: { customRender: 'action' },
  },
];

function fetchFamilyMembers() {
  // axios.get(`/api/familyMembers?teacher_id=${user.id}`).then(response => {
  //   familyMembers.value = response.data;
  // });

  // 模拟数据
  familyMembers.value = [
    {
      family_id: 'F01',
      relationship: '配偶',
      name: '王女士',
      gender: 'F',
      birth: '1980-05-15',
      id_number: '123456789012345678',
    },
  ];
}

function showAddModal() {
  modalTitle.value = '新增家属';
  isEdit.value = false;
  Object.assign(currentFamilyMember, {
    family_id: '',
    id: user.id,
    relationship: '',
    name: '',
    gender: '',
    birth: null,
    id_number: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑家属';
  isEdit.value = true;
  Object.assign(currentFamilyMember, record);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.familyForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新家属信息
      message.success('更新家属信息成功');
    } else {
      // 调用后端API新增家属
      message.success('新增家属成功');
    }
    isModalVisible.value = false;
    fetchFamilyMembers();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteFamilyMember(family_id) {
  // 调用后端API删除家属
  message.success('删除家属成功');
  fetchFamilyMembers();
}

onMounted(() => {
  fetchFamilyMembers();
});
</script>

<style scoped>
.family-management-page {
  padding: 24px;
}

.action-bar {
  margin-bottom: 16px;
}
</style>
