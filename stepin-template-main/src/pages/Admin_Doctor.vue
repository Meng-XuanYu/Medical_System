<template>
  <div>
    <h1>医生信息管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入医工号或姓名"
          @search="fetchDoctors"
          enter-button
      />
      <a-button type="primary" @click="showAddModal">新增医生</a-button>
    </div>
    <a-table :columns="columns" :data-source="doctors" row-key="staff_id">
      <template #image="{ text }">
        <img :src="getImagePath(text)" alt="医生图片" width="50" />
      </template>
      <template #action="{ record }">
        <a-button type="link" @click="showEditModal(record)">编辑</a-button>
        <a-button type="link" @click="deleteDoctor(record.staff_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 新增/编辑医生信息的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="modalTitle"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentDoctor"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="doctorForm"
      >
        <a-form-item label="医工号" :rules="[{ required: true, message: '请输入医工号' }]">
          <a-input v-model="currentDoctor.staff_id" :disabled="isEdit" />
        </a-form-item>
        <a-form-item label="密码" :rules="[{ required: true, message: '请输入密码' }]">
          <a-input v-model="currentDoctor.password" type="password" />
        </a-form-item>
        <a-form-item label="姓名" :rules="[{ required: true, message: '请输入姓名' }]">
          <a-input v-model="currentDoctor.name" />
        </a-form-item>
        <a-form-item label="性别" :rules="[{ required: true, message: '请选择性别' }]">
          <a-select v-model="currentDoctor.gender">
            <a-select-option value="男">男</a-select-option>
            <a-select-option value="女">女</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="职称" :rules="[{ required: true, message: '请输入职称' }]">
          <a-input v-model="currentDoctor.title" />
        </a-form-item>
        <a-form-item label="介绍" :rules="[{ required: true, message: '请输入介绍' }]">
          <a-textarea v-model="currentDoctor.introduction" rows="3" />
        </a-form-item>
        <!-- 图片上传 -->
        <a-form-item label="图片">
          <a-upload
              :action="uploadUrl"
              list-type="picture-card"
              :show-upload-list="false"
              @change="handleImageChange"
          >
            <img v-if="currentDoctor.image_path" :src="currentDoctor.image_path" alt="医生图片" style="width: 100%" />
            <div v-else>
              <a-icon type="plus" />
              <div style="margin-top: 8px">上传</div>
            </div>
          </a-upload>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const doctors = ref([]);
const isModalVisible = ref(false);
const modalTitle = ref('新增医生');
const isEdit = ref(false);
const currentDoctor = reactive({
  staff_id: '',
  password: '',
  name: '',
  gender: '',
  title: '',
  introduction: '',
  image_id: '',
  image_path: '',
});

const columns = [
  { title: '医工号', dataIndex: 'staff_id', key: 'staff_id' },
  { title: '姓名', dataIndex: 'name', key: 'name' },
  { title: '性别', dataIndex: 'gender', key: 'gender' },
  { title: '职称', dataIndex: 'title', key: 'title' },
  {
    title: '图片',
    dataIndex: 'image_id',
    key: 'image_id',
    scopedSlots: { customRender: 'image' },
  },
  { title: '介绍', dataIndex: 'introduction', key: 'introduction' },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
];

const uploadUrl = '/api/uploadImage'; // 图片上传接口

function getImagePath(image_id) {
  // 根据图片号获取图片路径
  // 这里假设后端提供了根据 image_id 获取图片路径的接口
  return `/api/getImage/${image_id}`;
}

function fetchDoctors() {
  // 调用后端API获取医生信息，支持搜索
  // 使用searchText.value作为搜索条件
  // 这里模拟数据
  doctors.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showAddModal() {
  modalTitle.value = '新增医生';
  isEdit.value = false;
  Object.assign(currentDoctor, {
    staff_id: '',
    password: '',
    name: '',
    gender: '',
    title: '',
    introduction: '',
    image_id: '',
    image_path: '',
  });
  isModalVisible.value = true;
}

function showEditModal(record) {
  modalTitle.value = '编辑医生';
  isEdit.value = true;
  Object.assign(currentDoctor, record);
  currentDoctor.image_path = getImagePath(record.image_id);
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.doctorForm;
  form.validateFields().then(async () => {
    if (isEdit.value) {
      // 调用后端API更新医生信息
      message.success('更新医生信息成功');
    } else {
      // 调用后端API新增医生
      message.success('新增医生成功');
    }
    isModalVisible.value = false;
    fetchDoctors();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteDoctor(staff_id) {
  // 调用后端API删除医生
  message.success('删除医生成功');
  fetchDoctors();
}

function handleImageChange(info) {
  if (info.file.status === 'done') {
    // 上传成功，获取图片ID和路径
    const response = info.file.response;
    currentDoctor.image_id = response.image_id;
    currentDoctor.image_path = response.image_path;
    message.success('图片上传成功');
  } else if (info.file.status === 'error') {
    message.error('图片上传失败');
  }
}

onMounted(() => {
  fetchDoctors();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
