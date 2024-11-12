<template>
  <div>
    <h1>家属管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入家属号、学工号或姓名"
          @search="fetchFamilyMembers"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增家属</a-button>
    </div>
    <a-table :columns="columns" :data-source="familyMembers" :row-key="record => record.family_id + '-' + record.id">
      <template #gender="{ text }">
        <span>{{ text === 'M' ? '男' : '女' }}</span>
      </template>
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteFamilyMember(record.family_id, record.id)">删除</a-button>
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
        <a-form-item label="学工号" :rules="[{ required: true, message: '请输入学工号' }]">
          <a-input v-model="currentFamilyMember.id" :disabled="isEdit" />
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

const searchText = ref('');
const familyMembers = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增家属');
const isEdit = ref(false);
const currentFamilyMember = reactive({
  family_id: '',
  id: '',
  relationship: '',
  name: '',
  gender: '',
  birth: null,
  id_number: '',
});

const columns = [
  { title: '家属号', dataIndex: 'family_id', key: 'family_id' },
  { title: '学工号', dataIndex: 'id', key: 'id' },
  { title: '关系', dataIndex: 'relationship', key: 'relationship' },
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '性别', dataIndex: 'gender', key: 'gender', scopedSlots: { customRender: 'gender' } },
  { title: '出生日期', dataIndex: 'birth', key: 'birth' },
  { title: '身份证号', dataIndex: 'id_number', key: 'id_number' },
  {
    title: '操作',
    key: 'action',
    width: 120,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchFamilyMembers() {
  // 调用后端API获取家属信息，支持搜索
  familyMembers.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增家属';
  isEdit.value = false;
  Object.assign(currentFamilyMember, {
    family_id: '',
    id: '',
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

function deleteFamilyMember(family_id, id) {
  // 调用后端API删除家属
  message.success('删除家属成功');
  fetchFamilyMembers();
}

onMounted(() => {
  fetchFamilyMembers();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
