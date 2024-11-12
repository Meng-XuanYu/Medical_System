<template>
  <div>
    <h1>图片管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入图片号"
          @search="fetchImages"
          enter-button
      />
      <a-button type="primary" @click="showUploadModal">上传图片</a-button>
    </div>
    <a-table :columns="columns" :data-source="images" row-key="image_id">
      <template #image_path="{ text }">
        <img :src="text" alt="图片" width="50" />
      </template>
      <template #action="{ record }">
        <a-button type="link" @click="deleteImage(record.image_id)">删除</a-button>
      </template>
    </a-table>

    <!-- 上传图片的模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        title="上传图片"
        @ok="handleOk"
        @cancel="handleCancel"
    >
      <a-form
          :model="currentImage"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          ref="imageForm"
      >
        <a-form-item label="图片文件" :rules="[{ required: true, message: '请上传图片' }]">
          <a-upload
              :action="uploadUrl"
              list-type="picture"
              :file-list="fileList"
              :before-upload="beforeUpload"
              @change="handleImageChange"
          >
            <a-button icon="upload">点击上传</a-button>
          </a-upload>
        </a-form-item>
        <a-form-item label="关联类型">
          <a-select v-model="currentImage.associationType">
            <a-select-option value="evaluation">评价</a-select-option>
            <a-select-option value="notification">通知</a-select-option>
            <a-select-option value="drug">药品</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="关联ID">
          <a-input v-model="currentImage.associationId" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const images = ref([]);
const isModalVisible = ref(false);
const currentImage = reactive({
  image_id: '',
  image_path: '',
  evaluation_id: '',
  notification_id: '',
  drug_id: '',
  associationType: '',
  associationId: '',
});
const fileList = ref([]);

const columns = [
  { title: '图片号', dataIndex: 'image_id', key: 'image_id' },
  {
    title: '图片',
    dataIndex: 'image_path',
    key: 'image_path',
    scopedSlots: { customRender: 'image_path' },
  },
  { title: '评价号', dataIndex: 'evaluation_id', key: 'evaluation_id' },
  { title: '通知号', dataIndex: 'notification_id', key: 'notification_id' },
  { title: '药品号', dataIndex: 'drug_id', key: 'drug_id' },
  {
    title: '操作',
    key: 'action',
    fixed: 'right',
    width: 80,
    scopedSlots: { customRender: 'action' },
  },
];

const uploadUrl = '/api/uploadImage'; // 图片上传接口

function fetchImages() {
  // 调用后端API获取图片信息，支持搜索
  images.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function showUploadModal() {
  Object.assign(currentImage, {
    image_id: '',
    image_path: '',
    evaluation_id: '',
    notification_id: '',
    drug_id: '',
    associationType: '',
    associationId: '',
  });
  fileList.value = [];
  isModalVisible.value = true;
}

function handleOk() {
  const form = this.$refs.imageForm;
  form.validateFields().then(async () => {
    // 根据关联类型设置对应的关联ID
    if (currentImage.associationType === 'evaluation') {
      currentImage.evaluation_id = currentImage.associationId;
    } else if (currentImage.associationType === 'notification') {
      currentImage.notification_id = currentImage.associationId;
    } else if (currentImage.associationType === 'drug') {
      currentImage.drug_id = currentImage.associationId;
    }
    // 调用后端API保存图片信息
    message.success('图片上传成功');
    isModalVisible.value = false;
    fetchImages();
  });
}

function handleCancel() {
  isModalVisible.value = false;
}

function deleteImage(image_id) {
  // 调用后端API删除图片
  message.success('删除图片成功');
  fetchImages();
}

function handleImageChange(info) {
  if (info.file.status === 'done') {
    // 上传成功，获取图片路径
    const response = info.file.response;
    currentImage.image_id = response.image_id;
    currentImage.image_path = response.image_path;
    message.success('图片上传成功');
  } else if (info.file.status === 'error') {
    message.error('图片上传失败');
  }
}

function beforeUpload(file) {
  const isImage = file.type.startsWith('image/');
  if (!isImage) {
    message.error('只能上传图片文件');
  }
  return isImage;
}

onMounted(() => {
  fetchImages();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
