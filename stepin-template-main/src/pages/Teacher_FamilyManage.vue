<template>
  <div class="family-management">
    <h1 class="title">家属信息管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入姓名或关系"
          @search="fetchFamilyMembers"
          enter-button
          class="search-input"
          allow-clear
      />
      <a-button type="primary" @click="showAddModal" class="add-button">
        <template #icon>
          <PlusOutlined />
        </template>
        新增家属
      </a-button>
    </div>
    <a-table
        :columns="columns"
        :dataSource="familyMembers"
        :pagination="pagination"
        :loading="loading"
        :rowKey="record => `${record.family_id}-${record.id}`"
        class="family-table"
        @change="handleTableChange"
    >
      <!-- 自定义渲染性别列 -->
      <template #bodyCell="{ column, record }">
        <template v-if="column.dataIndex === 'gender'">
          <span>{{ record.gender === 'M' ? '男' : '女' }}</span>
        </template>
        <!-- 自定义渲染操作列 -->
        <template v-else-if="column.key === 'actions'">
          <a-space>
            <a-button type="link" @click="showEditModal(record)">
              <EditOutlined /> 编辑
            </a-button>
            <a-button type="link" danger @click="deleteFamilyMember(record)">
              <DeleteOutlined /> 删除
            </a-button>
          </a-space>
        </template>
      </template>
    </a-table>

    <!-- 新增/编辑家属信息的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
        ok-text="确认"
        cancel-text="取消"
        centered
        style="top: 20px"
    >
      <a-form
          :form="form"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="familyForm"
          class="family-form"
      >
        <a-form-item label="家属号">
          <a-input v-model:value="currentFamilyMember.family_id" disabled />
        </a-form-item>
        <a-form-item label="学工号">
          <a-input v-model:value="currentFamilyMember.id" disabled />
        </a-form-item>
        <a-form-item
            label="关系"
            name="relationship"
            :rules="[{ required: true, message: '请输入关系' }]"
        >
          <a-input v-model:value="currentFamilyMember.relationship" />
        </a-form-item>
        <a-form-item
            label="姓名"
            name="name"
            :rules="[{ required: true, message: '请输入姓名' }]"
        >
          <a-input v-model:value="currentFamilyMember.name" />
        </a-form-item>
        <a-form-item
            label="性别"
            name="gender"
            :rules="[{ required: true, message: '请选择性别' }]"
        >
          <a-select v-model:value="currentFamilyMember.gender">
            <a-select-option value="M">男</a-select-option>
            <a-select-option value="F">女</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item
            label="出生日期"
            name="birth_date"
            :rules="[{ required: true, message: '请选择出生日期' }]"
        >
          <a-date-picker
              v-model:value="currentFamilyMember.birth_date"
              format="YYYY-MM-DD"
          />
        </a-form-item>
        <a-form-item
            label="身份证号"
            name="id_number"
            :rules="[
            { required: true, message: '请输入身份证号' },
            { len: 18, message: '身份证号应为18位' },
          ]"
        >
          <a-input v-model:value="currentFamilyMember.id_number" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { message, Modal, Form } from 'ant-design-vue';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
} from '@ant-design/icons-vue';
import http from '@/store/http';

interface FamilyMember {
  family_id: string;
  id: string;
  relationship: string;
  name: string;
  gender: string;
  birth_date: string;
  id_number: string;
}

const searchText = ref('');
const familyMembers = ref<FamilyMember[]>([]);
const loading = ref(false);
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
});
const isModalVisible = ref(false);
const modalTitle = ref('新增家属');
const isEditMode = ref(false);
const formRef = ref(null);
const form = Form.useForm(formRef);

const currentFamilyMember = reactive<FamilyMember>({
  family_id: '',
  id: '',
  relationship: '',
  name: '',
  gender: '',
  birth_date: '',
  id_number: '',
});

const columns = [
  {
    title: '关系',
    dataIndex: 'relationship',
    key: 'relationship',
  },
  {
    title: '姓名',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '性别',
    dataIndex: 'gender',
    key: 'gender',
    customRender: 'gender',
  },
  {
    title: '出生日期',
    dataIndex: 'birth_date',
    key: 'birth_date',
  },
  {
    title: '身份证号',
    dataIndex: 'id_number',
    key: 'id_number',
  },
  {
    title: '操作',
    key: 'actions',
    customRender: 'actions',
  },
];

function fetchFamilyMembers() {
  loading.value = true;
  http
      .request('/teacher/family_members/info/', 'get', {
        search: searchText.value,
      })
      .then((response) => {
        familyMembers.value = response.data.data;
        pagination.total = response.data.total;
      })
      .catch((error) => {
        message.error('获取家属信息失败');
        console.error(error);
      })
      .finally(() => {
        loading.value = false;
      });
}

function handleTableChange() {
  fetchFamilyMembers();
}

function showAddModal() {
  modalTitle.value = '新增家属';
  isEditMode.value = false;
  Object.assign(currentFamilyMember, {
    family_id: '',
    id: '',
    relationship: '',
    name: '',
    gender: '',
    birth_date: '',
    id_number: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record: FamilyMember) {
  modalTitle.value = '编辑家属信息';
  isEditMode.value = true;
  Object.assign(currentFamilyMember, record);
  isModalVisible.value = true;
}

function handleOk() {
        if (isEditMode.value) {
          // 编辑家属信息
          http
              .request('/teacher/family_members/update/', 'post_json', {
                ...currentFamilyMember,
              })
              .then(() => {
                message.success('家属信息更新成功');
                fetchFamilyMembers();
                isModalVisible.value = false;
                form.resetFields();
              })
              .catch((error) => {
                message.error('家属信息更新失败');
                console.error(error);
              });
        } else {
          // 新增家属信息，不需要传 family_id 和 id，后端处理
          const payload = { ...currentFamilyMember };
          delete payload.family_id;
          delete payload.id;
          http
              .request('/teacher/family_members/add/', 'post_json', { ...payload })
              .then(() => {
                message.success('家属信息添加成功');
                fetchFamilyMembers();
                isModalVisible.value = false;
                form.resetFields();
              })
              .catch((error) => {
                message.error('家属信息添加失败');
                console.error(error);
              });
        }

}

function handleCancel() {
  isModalVisible.value = false;
  form.resetFields();
}

function deleteFamilyMember(record: FamilyMember) {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除家属 ${record.name} 吗？`,
    okText: '确认',
    cancelText: '取消',
    onOk() {
      http
          .request('/teacher/family_members/delete/', 'post_json', {
            family_id: record.family_id,
            id: record.id,
          })
          .then(() => {
            message.success('家属信息删除成功');
            fetchFamilyMembers();
          })
          .catch((error) => {
            message.error('家属信息删除失败');
            console.error(error);
          });
    },
  });
}

onMounted(() => {
  fetchFamilyMembers();
});
</script>
<style scoped>
.family-management {
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2em;
  color: #1890ff;
}

.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.add-button {
  margin-left: auto;
}

.family-table .ant-table-thead > tr > th {
  background-color: #fafafa;
  font-weight: bold;
}

.family-form {
  margin-top: 20px;
}
</style>
