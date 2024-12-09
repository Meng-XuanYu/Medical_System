<template>
  <div class="admin-page">
    <h1 class="title">排班管理</h1>

    <!-- 科室列表视图 -->
    <div v-if="currentView === 'departments'" class="departments-view">
      <a-input-search
          v-model="searchText"
          placeholder="请输入科室号���科室名"
          @search="searchDepartments"
          enter-button
          class="search-input"
      />
      <div class="department-list">
        <div v-for="department in departments" :key="department.department_id" class="department-item" @click="selectDepartment(department)">
          <strong>{{ department.department_id }}</strong> - {{ department.department_name }}
        </div>
      </div>
      <a-button type="primary" @click="fetchSchedules" class="view-schedules-button">
        查看所有排班
      </a-button>
    </div>

    <!-- 医生选择视图 -->
    <div v-else-if="currentView === 'doctors'" class="doctors-view">
      <h2>选择医生 - {{ selectedDepartment.department_name }}</h2>
      <div class="doctor-list">
        <div v-for="doctor in doctors" :key="doctor.doctor_id" class="doctor-card" @click="selectDoctor(doctor)">
          <img :src="doctor.image" alt="头像" class="doctor-avatar"/>
          <p>{{ doctor.name }}</p>
        </div>
      </div>
      <a-button @click="backToDepartments" class="back-button">
        返回科室列表
      </a-button>
    </div>

    <div v-else-if="currentView === 'scheduleForm'" class="schedule-form-view">
      <h2>{{ isEdit ? '编辑排班' : '新增排班' }}</h2>
      <a-form :model="currentSchedule" :rules="scheduleRules" ref="scheduleForm">
        <a-form-item label="排班号" name="schedule_id" v-if="!isEdit">
          <span class="lspan"/>
          <a-input v-model:value="currentSchedule.schedule_id" />
        </a-form-item>
        <span class="span"/>

        <a-form-item label="医生" name="doctor">
          <div class="selected-doctor">
            <span><strong>{{ getDoctorName(currentSchedule.doctor) }}</strong></span>
            <img :src="getDoctorImage(currentSchedule.doctor)" alt="头像" width="120px" height="120px" />

          </div>
        </a-form-item>
        <a-form-item label="排班时间" name="schedule_time" rules="[ { required: true, placeholder: '请输入排班时间 data-startTime-endTime' } ]">
          <a-input v-model:value="currentSchedule.schedule_time" />
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="handleSubmit">{{ isEdit ? '确认编辑' : '确认添加' }}</a-button>
          <a-button @click="cancelScheduleForm" style="margin-left: 8px;">取消</a-button>
        </a-form-item>
      </a-form>
    </div>

    <!-- 排班列表视图 -->
    <div v-else-if="currentView === 'schedules'" class="schedules-view">
      <a-table :columns="scheduleColumns" :dataSource="schedules" rowKey="schedule_id">
        <template #actions="{ record }">
          <a-button type="link" @click="editSchedule(record)">
            <EditOutlined /> 编辑
          </a-button>
          <a-button type="link" @click="deleteSchedule(record.schedule_id)" danger>
            <DeleteOutlined /> 删除
          </a-button>
        </template>
      </a-table>
      <a-button @click="backToDepartments" class="back-button">
        返回科室列表
      </a-button>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { ref, reactive, onMounted, computed } from 'vue';
import { message } from 'ant-design-vue';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import http from "@/store/http";
async function getImage(image: string) {
  try {
    const response = await http.request('getImageUrl/', 'GET', { image: image });
    console.log(response.data.data as string);
    return response.data.data as string;
  } catch (error) {
    console.error('Error fetching image:', error);
    throw error;  // 或者根据需要处理错误
  }
}
// 当前视图状态：'departments', 'doctors', 'scheduleForm', 'schedules'
const currentView = ref<'departments' | 'doctors' | 'scheduleForm' | 'schedules'>('departments');

// 搜索文本
const searchText = ref('');

// 科室数据
const departments = ref<{ department_id: string, department_name: string }[]>([]);

// 选择的科室
const selectedDepartment = reactive<{ department_id: string, department_name: string }>({ department_id: '', department_name: '' });

// 医生数据
const doctors = ref<{ doctor_id: string, name: string, image: string, department_id: string }[]>([]);



// 排班数据
const schedules = ref<{ schedule_id: string, doctor: string, department: string, schedule_time: string, doctor_name: string, department_name: string }[]>([]);

// 当前排班（用于新增或编辑）
const currentSchedule = reactive({
  schedule_id: '',
  doctor: '',
  department: '',
  schedule_time: ''
});

// 是否编辑模式
const isEdit = ref(false);

// 表单引用
const scheduleForm = ref(null);

// 排班表格列
const scheduleColumns = [
  { title: '排班号', dataIndex: 'schedule_id', key: 'schedule_id' },
  { title: '医生号', dataIndex: 'doctor', key: 'doctor' },
  { title: '科室号', dataIndex: 'department', key: 'department' },
  { title: '排班时间', dataIndex: 'schedule_time', key: 'schedule_time' },
  { title: '操作', key: 'actions', slots: { customRender: 'actions' } },
];

// 表单验证规则
const scheduleRules = {
  doctor_id: [
    { required: true, message: '请选择医生', trigger: 'change' }
  ],
  schedule_time: [
    { required: true, message: '请输入排班时间', trigger: 'change' }
  ],
};
function getDoctorImage(doctor_id: string) {
  const doctor = doctors.value.find(doc => doc.doctor_id === doctor_id);
  return doctor ? doctor.image : '';
}

// 获取科室列表
async function fetchDepartments() {
  try {
    const response = await http.request('/department/all/', 'POST_JSON', {});
    departments.value = response.data;
  } catch (error) {
    message.error('获取科室列表失败');
  }
}

// 获取所有医生列表
async function fetchAllDoctors() {
  try {
    const response = await http.request('/staff/all/', 'POST_JSON', {});
    doctors.value = response.data;
    doctors.value.forEach(async (item: any) => {
      item.image = await getImage(item.image);
    });
  } catch (error) {
    message.error('获取医生列表失败');
  }
}

// 获取排班列表
async function fetchSchedules() {
  try {
    const response = await http.request('/schedule/all/', 'POST_JSON', {});
    schedules.value = response.data.map((sched: any) => ({
      ...sched,
      doctor_name: getDoctorName(sched.doctor_id),
      department_name: getDepartmentName(sched.department_id)
    }));
    currentView.value = 'schedules';
  } catch (error) {
    message.error('获取排班列表失败');
  }
}

// 获取医生姓名
function getDoctorName(doctor_id: string): string {
  const doctor = doctors.value.find(doc => doc.doctor_id === doctor_id);
  return doctor ? doctor.name : '未知';
}

// 获取科室名称
function getDepartmentName(department_id: string): string {
  const dept = departments.value.find(d => d.department_id === department_id);
  return dept ? dept.department_name : '未知';
}

// 搜索科室
function searchDepartments() {
  // 过滤逻辑已经在 computed 中处理
}

// 选择科室
function selectDepartment(department: { department_id: string, department_name: string }) {
  Object.assign(selectedDepartment, department);
  currentSchedule.department = department.department_id;
  currentView.value = 'doctors';
}

// 返回科室列表
function backToDepartments() {
  currentView.value = 'departments';
}

// 选择医生
function selectDoctor(doctor: { doctor_id: string, name: string, image: string, department_id: string }) {
  currentSchedule.doctor = doctor.doctor_id;
  isEdit.value = false;
  currentView.value = 'scheduleForm';
}

// 编辑排班
function editSchedule(record: any) {
  Object.assign(currentSchedule, record);
  isEdit.value = true;
  currentView.value = 'scheduleForm';
}

// 删除排班
async function deleteSchedule(schedule_id: string) {
  try {
    await http.request('/schedule/delete/', 'POST_JSON', { schedule_id });
    message.success('删除排班信息成功');
    await fetchSchedules();
  } catch (error) {
    message.error('删除排班信息失败');
  }
}

// 提交排班表单
async function handleSubmit() {
  try {
    await scheduleForm.value.validate();
    if (isEdit.value) {
      await http.request('/schedule/update/', 'POST_JSON', {
        schedule_id: currentSchedule.schedule_id,
        doctor_id: currentSchedule.doctor,
        schedule_time: currentSchedule.schedule_time,
        department_id: currentSchedule.department
      });
      message.success('编辑排班信息成功');
    } else {
      await http.request('/schedule/add/', 'POST_JSON', {schedule_id: currentSchedule.schedule_id,
        doctor_id: currentSchedule.doctor,
        schedule_time: currentSchedule.schedule_time,
        department_id: currentSchedule.department});
      message.success('新增排班信息成功');
    }
    currentView.value = 'departments';
    await fetchSchedules();
  } catch (error) {
    message.error('提交排班信息失败');
  }
}

// 取消排班表单
function cancelScheduleForm() {
  currentView.value = isEdit.value ? 'schedules' : 'doctors';
}

// 初始加载
onMounted(() => {
  fetchDepartments();
  fetchAllDoctors();
});
</script>

<style scoped>
.admin-page {
  padding: 20px;
  background-color: #f0f2f5;
  border-radius: 8px;
  font-family: 'Arial', sans-serif;
}

.title {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
  text-shadow: 1px 1px 2px #aaa;
}
 .schedule-form-view {

   max-width: 600px;
   margin: 0 auto;
   padding: 40px;
   background-color: #fff;
   border-radius: 8px;
   box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
 }

.schedule-form-view h2 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: lighter;
  text-align: center;
}

.selected-doctor {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.selected-doctor img {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}

.a-form-item {
  margin-bottom: 50px;
}

.a-button {
  width: 100%;
  margin-top: 10px;
}
.search-input {
  width: 400px;
  margin-bottom: 20px;
}

.department-list {
  margin-bottom: 20px;
}

.department-item {
  cursor: pointer;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  margin-bottom: 10px;
  background-color: #fff;
  transition: background-color 0.3s;
}

.department-item:hover {
  background-color: #e6f7ff;
}

.doctor-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 20px;
}
.span {
  display: block;
  margin-bottom: 30px;
}
.lspan {
  display: block;
  margin-left: 10px;
}
.doctor-card {
  cursor: pointer;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background-color: #fff;
  transition: background-color 0.3s;
  text-align: center;
  width: calc(25% - 16px);

}

.doctor-card:hover {
  background-color: #e6f7ff;
}

.doctor-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
}

.back-button {
  margin-top: 20px;
}

.view-schedules-button {
  margin-top: 20px;
}

.schedules-view {
  margin-top: 20px;
}


.schedule-form-view .doctor-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}

.schedule-form-view h2 {
  margin-bottom: 20px;
}
</style>