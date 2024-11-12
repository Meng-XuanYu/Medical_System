<!-- Payment.vue -->
<template>
  <div class="payment-page">
    <h1>在线缴费</h1>
    <div v-if="pendingPayments.length > 0">
      <a-table :columns="columns" :data-source="pendingPayments" row-key="payment_id">
        <template #action="{ record }">
          <a-button type="primary" @click="showPaymentModal(record)">支付</a-button>
        </template>
      </a-table>
    </div>
    <div v-else>
      <p>当前没有待缴费项目</p>
    </div>

    <!-- 支付模态框 -->
    <a-modal
        v-model:visible="isModalVisible"
        :title="'支付 - ' + currentPayment.project_name"
        @cancel="handleCancel"
        footer={null}
    >
      <p>请选择支付方式：</p>
      <div class="payment-methods">
        <a-button type="default" @click="handlePayment('wechat')">
          <img src="wechat.png" alt="微信支付" width="24" />
          微信支付
        </a-button>
        <a-button type="default" @click="handlePayment('alipay')">
          <img src="alipay.png" alt="支付宝支付" width="24" />
          支付宝支付
        </a-button>
      </div>
      <div v-if="showQRCode" class="qr-code">
        <p>请使用手机扫码完成支付</p>
        <img src="qr_code_placeholder.png" alt="二维码" width="200" />
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';

const user = {
  id: 'S1234567',
};

const pendingPayments = ref([]);
const isModalVisible = ref(false);
const currentPayment = reactive({});
const showQRCode = ref(false);

const columns = [
  { title: '项目', dataIndex: 'project_name', key: 'project_name' },
  { title: '金额', dataIndex: 'amount', key: 'amount' },
  {
    title: '操作',
    key: 'action',
    width: 100,
    slots: { customRender: 'action' },
  },
];

function fetchPendingPayments() {
  // axios.get(`/api/payments?user_id=${user.id}`).then(response => {
  //   pendingPayments.value = response.data;
  // });

  // 模拟数据
  pendingPayments.value = [
    { payment_id: 'P001', project_name: '挂号费', amount: 10 },
    { payment_id: 'P002', project_name: '药费', amount: 50 },
  ];
}

function showPaymentModal(payment) {
  Object.assign(currentPayment, payment);
  isModalVisible.value = true;
  showQRCode.value = false;
}

function handleCancel() {
  isModalVisible.value = false;
  showQRCode.value = false;
}

function handlePayment(method) {
  // 显示二维码
  showQRCode.value = true;

  // 模拟支付成功后回调
  setTimeout(() => {
    message.success('支付成功');
    isModalVisible.value = false;
    showQRCode.value = false;
    // 通知后端更新支付状态和药品信息等
    // axios.post('/api/payments/complete', { payment_id: currentPayment.payment_id }).then(() => {
    //   fetchPendingPayments();
    // });
    fetchPendingPayments();
  }, 3000);
}

onMounted(() => {
  fetchPendingPayments();
});
</script>

<style scoped>
.payment-page {
  padding: 24px;
}

.payment-methods {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}

.payment-methods a-button {
  display: flex;
  align-items: center;
  gap: 8px;
}

.qr-code {
  margin-top: 24px;
  text-align: center;
}
</style>
