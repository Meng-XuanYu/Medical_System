<!-- HealthRecords.vue -->
<template>
  <div class="health-records-page">
    <h1>健康档案</h1>
    <a-tabs default-active-key="physicalExam">
      <a-tab-pane key="physicalExam" tab="体检记录">
        <a-table :columns="physicalExamColumns" :data-source="physicalExams" row-key="exam_id">
          <template #details="{ record }">
            <a-button type="link" @click="viewExamDetails(record)">查看详情</a-button>
          </template>
        </a-table>
      </a-tab-pane>
      <a-tab-pane key="medicalRecords" tab="病历">
        <a-table :columns="medicalRecordColumns" :data-source="medicalRecords" row-key="medical_record_id">
          <template #details="{ record }">
            <a-button type="link" @click="viewMedicalRecordDetails(record)">查看详情</a-button>
          </template>
        </a-table>
      </a-tab-pane>
      <a-tab-pane key="appointments" tab="就诊记录">
        <a-table :columns="appointmentColumns" :data-source="appointments" row-key="appointment_id">
          <template #details="{ record }">
            <a-button type="link" @click="viewAppointmentDetails(record)">查看详情</a-button>
          </template>
        </a-table>
      </a-tab-pane>
      <a-tab-pane key="prescriptions" tab="处方">
        <a-table :columns="prescriptionColumns" :data-source="prescriptions" row-key="prescription_id">
          <template #details="{ record }">
            <a-button type="link" @click="viewPrescriptionDetails(record)">查看详情</a-button>
          </template>
        </a-table>
      </a-tab-pane>
    </a-tabs>

    <!-- 详情模态框 -->
    <div
        v-if ="isModalVisible"
        :title="modalTitle"
        @cancel="handleModalCancel"
        class="floating-modal"
    >
      <div class="modal-header">
        <span>{{ modalTitle }}</span>
        <a-button type="link" @click="handleModalCancel">关闭</a-button>
      </div>
      <div v-html="modalContent"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';


const user = {
  id: 'S1234567',
  name: '张学生',
};

const physicalExams = ref([]);
const medicalRecords = ref([]);
const appointments = ref([]);
const prescriptions = ref([]);

const isModalVisible = ref(false);
const modalTitle = ref('');
const modalContent = ref('');

const physicalExamColumns = [
  { title: '体检编号', dataIndex: 'exam_id', key: 'exam_id' },
  { title: '体检日期', dataIndex: 'date', key: 'date' },
  { title: '体检项目', dataIndex: 'items', key: 'items' },
  { title: '操作', key: 'details', slots: { customRender: 'details' } },
];

const medicalRecordColumns = [
  { title: '病历号', dataIndex: 'medical_record_id', key: 'medical_record_id' },
  { title: '创建时间', dataIndex: 'create_time', key: 'create_time' },
  { title: '主诉', dataIndex: 'chief_complaint', key: 'chief_complaint' },
  { title: '操作', key: 'details', slots: { customRender: 'details' } },
];

const appointmentColumns = [
  { title: '预约号', dataIndex: 'appointment_id', key: 'appointment_id' },
  { title: '就诊日期', dataIndex: 'date', key: 'date' },
  { title: '医生', dataIndex: 'doctor_name', key: 'doctor_name' },
  { title: '科室', dataIndex: 'department_name', key: 'department_name' },
  { title: '操作', key: 'details', slots: { customRender: 'details' } },
];

const prescriptionColumns = [
  { title: '处方号', dataIndex: 'prescription_id', key: 'prescription_id' },
  { title: '开具日期', dataIndex: 'create_time', key: 'create_time' },
  { title: '医生', dataIndex: 'doctor_name', key: 'doctor_name' },
  { title: '操作', key: 'details', slots: { customRender: 'details' } },
];

function fetchPhysicalExams() {
  // axios.get(`/api/physicalExams?user_id=${user.id}`).then(response => {
  //   physicalExams.value = response.data;
  // });

  // 模拟数据
  physicalExams.value = [
    {
      exam_id: 'PE001',
      date: '2023-05-15',
      items: '血常规, 尿常规',
    },
  ];
}

function fetchMedicalRecords() {
  // axios.get(`/api/medicalRecords?user_id=${user.id}`).then(response => {
  //   medicalRecords.value = response.data;
  // });

  // 模拟数据
  medicalRecords.value = [
    {
      medical_record_id: 'MR001',
      create_time: '2023-06-10 09:00:00',
      chief_complaint: '咳嗽一周',
    },
  ];
}

function fetchAppointments() {
  // axios.get(`/api/appointments/history?user_id=${user.id}`).then(response => {
  //   appointments.value = response.data;
  // });

  // 模拟数据
  appointments.value = [
    {
      appointment_id: 'A002',
      date: '2023-06-10',
      doctor_name: '王医生',
      department_name: '内科',
    },
  ];
}

function fetchPrescriptions() {
  // axios.get(`/api/prescriptions?user_id=${user.id}`).then(response => {
  //   prescriptions.value = response.data;
  // });

  // 模拟数据
  prescriptions.value = [
    {
      prescription_id: 'P002',
      create_time: '2023-06-10 10:00:00',
      doctor_name: '王医生',
    },
  ];
}

function viewExamDetails(record) {
  modalTitle.value = `体检详情 - ${record.exam_id}`;
  // 构建详情内容
  modalContent.value = `
    <p><strong>体检日期：</strong>${record.date}</p>
    <p><strong>体检项目：</strong>${record.items}</p>
    <p><strong>体检结果：</strong>正常</p>
  `;
  isModalVisible.value = true;
}

function viewMedicalRecordDetails(record) {
  modalTitle.value = `病历详情 - ${record.medical_record_id}`;
  // 构建详情内容
  modalContent.value = `
    <p><strong>创建时间：</strong>${record.create_time}</p>
    <p><strong>主诉：</strong>${record.chief_complaint}</p>
    <p><strong>现病史：</strong>...</p>
    <p><strong>既往史：</strong>...</p>
    <p><strong>过敏史：</strong>...</p>
  `;
  isModalVisible.value = true;
}

function viewAppointmentDetails(record) {
  modalTitle.value = `就诊记录详情 - ${record.appointment_id}`;
  // 构建详情内容
  modalContent.value = `
    <p><strong>就诊日期：</strong>${record.date}</p>
    <p><strong>医生：</strong>${record.doctor_name}</p>
    <p><strong>科室：</strong>${record.department_name}</p>
    <p><strong>诊断：</strong>...</p>
  `;
  isModalVisible.value = true;
}

function viewPrescriptionDetails(record) {
  modalTitle.value = `处方详情 - ${record.prescription_id}`;
  // 构建详情内容
  modalContent.value = `
    <p><strong>开具日期：</strong>${record.create_time}</p>
    <p><strong>医生：</strong>${record.doctor_name}</p>
    <p><strong>药品列表：</strong></p>
    <ul>
      <li>阿司匹林 - 10片</li>
      <li>布洛芬 - 5片</li>
    </ul>
  `;
  isModalVisible.value = true;
}

function handleModalCancel() {
  isModalVisible.value = false;
}

onMounted(() => {
  fetchPhysicalExams();
  fetchMedicalRecords();
  fetchAppointments();
  fetchPrescriptions();
});
</script>

<style scoped>
.modal-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  cursor: move;
  font-size: 18px;
  font-weight: bold;
}
.floating-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 400px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 999;
  padding: 20px;
  overflow: hidden;
  cursor: move;

}
.health-records-page {
  padding: 24px;
}

.health-records-page h1 {
  margin-bottom: 24px;
}

.health-records-page .ant-tabs {
  margin-top: 16px;
}
</style>
