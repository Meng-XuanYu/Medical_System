<template>
  <div>
    <h1>评价管理</h1>
    <div class="search-bar">
      <a-input-search
          v-model="searchText"
          placeholder="请输入评价号、评价人学工号或被评价人医工号"
          @search="fetchEvaluations"
          enter-button
      />
    </div>
    <a-table :columns="columns" :data-source="evaluations" row-key="evaluation_id">
      <template #action="{ record }">
        <a-button type="link" @click="deleteEvaluation(record.evaluation_id)">删除</a-button>
      </template>
    </a-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';

const searchText = ref('');
const evaluations = ref([]);

const columns = [
  { title: '评价号', dataIndex: 'evaluation_id', key: 'evaluation_id' },
  { title: '评价内容', dataIndex: 'evaluation', key: 'evaluation' },
  { title: '评价时间', dataIndex: 'evaluation_time', key: 'evaluation_time' },
  { title: '评价人学工号', dataIndex: 'id', key: 'id' },
  { title: '被评价人医工号', dataIndex: 'staff_id', key: 'staff_id' },
  { title: '体检日期', dataIndex: 'examination_date', key: 'examination_date' },
  { title: '负责医工号', dataIndex: 'responsible_staff_id', key: 'responsible_staff_id' },
  {
    title: '操作',
    key: 'action',
    fixed: 'right',
    width: 80,
    scopedSlots: { customRender: 'action' },
  },
];

function fetchEvaluations() {
  // 调用后端API获取评价信息，支持搜索
  evaluations.value = [
    // 模拟数据，根据searchText过滤
  ];
}

function deleteEvaluation(evaluation_id) {
  // 调用后端API删除评价信息
  message.success('删除评价成功');
  fetchEvaluations();
}

onMounted(() => {
  fetchEvaluations();
});
</script>

<style scoped>
.search-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}
</style>
