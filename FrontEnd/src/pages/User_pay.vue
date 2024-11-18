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
    <div v-if="isModalVisible" class="floating-modal">
      <div class="modal-header">
        <span class="payhead">支付 - {{ currentPayment.payment_name }}</span>
        <a-button type="link" @click="handleCancel" class="shutbutton">关闭</a-button>
      </div>
      <div class="modal-body">

        <div class="payment-methods" v-if="!showQRCode">
          <a-button type="default" @click="handlePayment('wechat')" class="paybutton">
            <img src="@/assets/wechatpay.png" alt="微信支付" width="300"  />
          </a-button>
          <a-button type="default" @click="handlePayment('alipay')" class="paybutton">
            <img src="@/assets/alipay.png" alt="支付宝支付" width="300" height="140"/>
          </a-button>
        </div>
        <div v-if="showQRCode" class="qr-code">
          <p>请使用手机扫码完成支付</p>
          <img src="@/assets/qr_code_placeholder.png" alt="二维码" width="200" />
          <p v-if="remainingTime > 0">支付剩余时间：{{ remainingTime }} 秒</p>
          <p v-else>超时</p>
        </div>
      </div>
    </div>
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
const remainingTime = ref(300);
let countdownTimer = null;
let paymentStatusTimer = null;

const columns = [
  { title: '项目', dataIndex: 'payment_name', key: 'payment_name', width: 150 },
  { title: '描述', dataIndex: 'payment_description', key: 'payment_description',width: 400 },
  { title: '金额', dataIndex: 'amount', key: 'amount', width: 150 },
  {
    title: '操作',
    key: 'action',
    width: 100,
    slots: { customRender: 'action' },
  },
];

function fetchPendingPayments() {
  /*axios.get(`/api/payments?user_id=${user.id}`).then(response => {
    pendingPayments.value = response.data;
  });*/
  pendingPayments.value = [
    {  payment_name: '挂号费',      payment_description: '11月17日下午4点的预约',  amount: 10 },
    { payment_name: '药费',       payment_description:'阿司匹林 ；两盒', amount: 40 },
    {  payment_name: '药费',payment_description:'头孢克肟  一盒', amount: 30 },
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
  clearInterval(countdownTimer);
  clearInterval(paymentStatusTimer);
  message.warning('支付取消');
}

function startCountdown() {
  countdownTimer = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--;
    } else {
      clearInterval(countdownTimer);
      clearInterval(paymentStatusTimer);
      message.error('支付超时');
      isModalVisible.value = false;
      showQRCode.value = false;
    }
  }, 1000);
}

function checkPaymentStatus() {
  paymentStatusTimer = setInterval(() => {
    axios.get(`/api/payments/status?payment_id=${currentPayment.payment_id}`).then(response => {
      if (response.data.status === 'success') {
        message.success('支付成功');
        isModalVisible.value = false;
        showQRCode.value = false;
        clearInterval(countdownTimer);
        clearInterval(paymentStatusTimer);
        fetchPendingPayments();
      }
    });
  }, 2000);
}

function handlePayment() {
  // 显示二维码
  showQRCode.value = true;
  remainingTime.value = 300;


    // 开始倒计时
    startCountdown();
    // 检查支付状态
    checkPaymentStatus();

}

onMounted(() => {
  fetchPendingPayments();
});
</script>

<style scoped>
.payment-page {


  margin: 0 ;
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
  font-family: 'Arial', sans-serif;
}

.payment-page h1 {
  text-align: center;
  margin-bottom: 24px;
}

.payment-methods {

  flex-direction: column;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
}

.payment-methods a-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
}

.qr-code {
  margin-top: 24px;
  text-align: center;
}

.qr-code img {
  border: 1px solid #f0f0f0;
  padding: 8px;
  background-color: #fff;
}

.floating-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 380px;
  height: 450px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  z-index: 999;
  overflow: visible;
}

.modal-header {
  background-color: #1890ff;
  color: #fff;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header a-button {
  color: #fff;
}

.modal-body {
  padding: 24px 16px;
}

.modal-body p {
  margin-bottom: 16px;
  font-size: 16px;
}
.paybutton {
  width: 350px;
  height: 150px;
  margin-bottom: 20px;
  border-radius: 8px;
}
.shutbutton {
    color: white;
    background-color: transparent;
    border: 1px solid white;
}
.payhead {
  font-size: 20px;
}
a-table {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}
</style>
