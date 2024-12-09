<template>
  <div class="appointment-schedule">
    <h1 class="title">预约排班信息</h1>
    <div class="search-container">
    <a-input-search
        v-model="searchText"
        placeholder="请输入科室名称、医生姓名"
        @search="fetchAppointmentInfo"
        enter-button
        class="search-input"
        allow-clear
    />
    <a-button type="primary" @click="showModal = true" class="view-appointments-button">
      查看我的预约记录
    </a-button>
    </div>
    <div v-if="showModal" class="floating-modal-another" title="我的预约记录" @ok="handleOkk" @cancel="handleCancel" width="800px">
      <a-table :columns="columns" :data-source="appointments" row-key="appointment_id">
        <template #state="{ record }">
          <span :class="getStateClass(record.state)">{{ record.state }}</span>
        </template>
        <template #action="{ record }">
          <a-button type="danger" @click="cancelAppointment(record)" :disabled="record.state === '已取消'">
            取消预约
          </a-button>
        </template>
      </a-table>
      <span class="myfooter">
        <button @click="showModal = false" class="cancel-button">返回</button>
      </span>
    </div>

    <a-spin :spinning="loading" tip="加载中...">
      <a-row :gutter="[16, 16]" class="department-container">
        <a-col
            v-for="(department, departmentIndex) in appointmentData"
            :key="departmentIndex"
            :span="24"
        >
          <a-card
              :hoverable="true"
              class="department-card"
          >
            <span class = "myhead">
              {{department.department}}
            </span>

            <a-collapse
                v-model:activeKey="activeDepartmentKeys[departmentIndex]"
                ghost
                accordion
                @click="toggleDepartment(departmentIndex)"
            >

              <a-collapse-panel
                  v-for="(doctor, doctorIndex) in department.doctors"
                  :key="doctorIndex"
                  class="mypanel"
                  :header="`${doctor.title} ${doctor.name} (${doctor.gender})`"
              >

                <a-row :gutter="[16, 16]" class="doctor-container">
                  <a-col :span="4">
                    <img
                        :src="doctor.image_id"
                        width="160"
                        class="doctor-avatar"
                    />
                  </a-col>
                  <a-col :span="20">
                    <div class="doctor-details">
                      <div class="doctor-info">
                        <div class="doctor-info-left">
                          <p><strong>姓名：</strong>{{ doctor.name }}</p>
                          <p><strong>性别：</strong>{{ doctor.gender }}</p>
                          <p><strong>职称：</strong>{{ doctor.title }}</p>
                        </div>
                        <div class="doctor-info-right">
                          <p class="doctor-introduction"><strong>简介：</strong>{{ doctor.introduction }}</p>
                        </div>
                      </div>
                    </div>

                  </a-col>
                  <div class="schedule-times">
                    <h3>可预约时间段：</h3>
                    <a-row :gutter="[8, 8]">
                      <a-col
                          v-for="(timeSlot, timeIndex) in groupedScheduleTimes(doctor.schedule_times)"
                          :key="timeIndex"
                          :span="24"
                      >
                        <div class="time-slot-container">
                          <div class="date-title">{{ timeSlot.date }}</div>
                          <div class="time-slots">
                            <a-row :gutter="[8, 8]">
                              <a-col
                                  v-for="(time, idx) in timeSlot.times"
                                  :key="idx"
                                  :span="6"
                              >
                                <a-button
                                    type="primary"
                                    size="small"
                                    @click="bookAppointment(doctor,timeSlot.date,time.start, time.end, time.schedule_id)"
                                    block
                                    class="myabutton"
                                >
                                  <CalendarOutlined/>
                                  {{ formatTime(time.start) }} - {{ formatTime(time.end) }}
                                </a-button>
                              </a-col>
                            </a-row>
                          </div>
                        </div>
                      </a-col>
                    </a-row>
                  </div>
                </a-row>
              </a-collapse-panel>
            </a-collapse>
          </a-card>
        </a-col>
      </a-row>
    </a-spin>

    <div ref="modalRef" v-if="isModalVisible" class="floating-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>预约确认</h3>
          <button @click="isModalVisible = false" class="close-button">&times;</button>
        </div>
        <div class="modal-body">
          <p>
            你确定要预约 <strong>{{ selectedDoctor.name }}</strong> 在
            <strong>{{ selectedDate }}</strong> {{ formatTime(selectedTimeStart) }} - {{ formatTime(selectedTimeEnd) }}
            进行问诊吗？
          </p>
        </div>
        <div class="modal-footer">
          <button @click="confirmBooking" class="confirm-button">确认</button>
          <button @click="isModalVisible = false" class="cancel-button">取消</button>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, watch} from 'vue';
import {message} from 'ant-design-vue';
import {CalendarOutlined} from '@ant-design/icons-vue';
import http from '@/store/http';
const showModal = ref(false);
const appointments = ref([]);

const columns = [
  { title: '预约编号', dataIndex: 'appointment_id', key: 'appointment_id' },
  { title: '医生姓名', dataIndex: 'doctor_name', key: 'doctor_name' },
  { title: '预约时间', dataIndex: 'schedule_time', key: 'schedule_time' },
  { title: '状态', dataIndex: 'state', key: 'state', slots: { customRender: 'state' } },
  { title: '操作', key: 'action', slots: { customRender: 'action' } },
];

function getStateClass(state: string) {
  switch (state) {
    case '已取消':
      return 'state-cancelled';
    case '已完成':
      return 'state-completed';
    default:
      return 'state-active';
  }
}

async function fetchAppointments() {
  try {
    const response = await http.request('/user/appointment/info/', 'get', {
      relation: localStorage.getItem('relation'),
    }); // 根据实际 API 路径调整
    appointments.value = response.data.data.map((appointment: any) => ({
      appointment_id: appointment.appointment_id,
      doctor_name: appointment.doctor_name,
      schedule_time: appointment.schedule_time,
      state: appointment.state,
    }));
  } catch (error) {
    console.error('Failed to fetch appointments:', error);
  }
}
async function cancelAppointment(record: any) {
  try {
    const response = await http.request('/user/appointment/cancel/', 'POST_JSON', {
      relation: localStorage.getItem('relation'),
      appointment_id: record.appointment_id,
    });
    if (response.data.status === 'success') {
      message.success('取消预约成功');
      await fetchAppointments();
    } else {
      message.error(response.data.message || '取消预约失败');
    }
  } catch (error) {
    message.error('取消预约失败');
    console.error('Failed to cancel appointment:', error);
  }
}
function handleOkk() {
  showModal.value = false;
}

function handleCancel() {
  showModal.value = false;
}

watch(showModal, (newVal) => {
  if (newVal) {
    fetchAppointments();
  }
});
import {computed, CSSProperties,  watchEffect} from 'vue';
import {useDraggable} from '@vueuse/core';

const modalTitleRef = ref<HTMLElement>(null);
const selectedDate = ref('');
const selectedTimeStart = ref('');
const selectedTimeEnd = ref('');
const {x, y, isDragging} = useDraggable(modalTitleRef);
const handleOk = (e: MouseEvent) => {
  console.log(e);
  isModalVisible.value = false;
};
const startX = ref<number>(0);
const startY = ref<number>(0);
const startedDrag = ref(false);
const transformX = ref(0);
const transformY = ref(0);
const preTransformX = ref(0);
const preTransformY = ref(0);
const dragRect = ref({left: 0, right: 0, top: 0, bottom: 0});
watch([x, y], () => {
  if (!startedDrag.value) {
    startX.value = x.value;
    startY.value = y.value;
    const bodyRect = document.body.getBoundingClientRect();
    const titleRect = modalTitleRef.value.getBoundingClientRect();
    dragRect.value.right = bodyRect.width - titleRect.width;
    dragRect.value.bottom = bodyRect.height - titleRect.height;
    preTransformX.value = transformX.value;
    preTransformY.value = transformY.value;
  }
  startedDrag.value = true;
});
watch(isDragging, () => {
  if (!isDragging) {
    startedDrag.value = false;
  }
});

watchEffect(() => {
  if (startedDrag.value) {
    transformX.value =
        preTransformX.value +
        Math.min(Math.max(dragRect.value.left, x.value), dragRect.value.right) -
        startX.value;
    transformY.value =
        preTransformY.value +
        Math.min(Math.max(dragRect.value.top, y.value), dragRect.value.bottom) -
        startY.value;
  }
});

const transformStyle = computed<CSSProperties>(() => {
  return {
    transform: `translate(${transformX.value}px, ${transformY.value}px)`,
  };
});

interface TimeSlot {
  date: string;
  times: { start: string; end: string, schedule_id: string }[];
}

interface Doctor {
  name: string;
  gender: string;
  title: string;
  image_id: string;
  doctor_id: string;
  introduction: string;
  schedule_times: {}; // 格式: 'YYYY-MM-DD-HHMM-HHMM'
}

interface Department {
  department: string;
  doctors: Doctor[];
}

const appointmentData = ref<Department[]>([]);
const searchText = ref('');
const loading = ref(false);

// 控制哪些科室被展开
const activeDepartmentKeys = ref<(string | string[])[]>([]);

// 预约确认模态框状态
const isModalVisible = ref(false);
const selectedDoctor = ref<Doctor | null>(null);
const selectedschedule = ref<string | null>(null);

async function fetchAppointmentInfo() {
  loading.value = true;
  try {
    const response = await http.request('/appointment/info/', 'get'); // 根据实际 API 路径调整
    appointmentData.value = response.data.data;
    appointmentData.value.forEach((department) => {
      department.doctors.forEach(async (doctor) => {
        doctor.image_id = await getImage(doctor.image_id);
      });
    });
    message.success('加载成功');
  } catch (error) {
    message.error('获取预约排班信息失败');
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 格式化时间，例如 "0800" => "08:00"
function formatTime(time: string): string {
  if (time.length !== 4) return time;
  return `${time.slice(0, 2)}:${time.slice(2, 4)}`;
}

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

// 解析并分组时间段
function groupedScheduleTimes(schedule_times: {}): TimeSlot[] {
  const groups: { [key: string]: { start: string; end: string; schedule_id: string }[] } = {};

  for (const [key, value] of Object.entries(schedule_times)) {
    const [date, start, end] = String(value).split('-');
    if (!groups[date]) {
      groups[date] = [];
    }
    let schedule_id = key;
    groups[date].push({start, end, schedule_id});
  }

  // 将结果中的 `times` 从 `{start, end}` 转换为 `TimeSlot[]`
  return Object.keys(groups)
      .sort()
      .map((date) => ({
        date,
        times: groups[date],
      }));
}

// 预约函数
function bookAppointment(
    doctor: Doctor,
    date: string,
    start: string,
    end: string,
    schedule_id: string,
) {
  selectedDoctor.value = doctor;
  selectedschedule.value = schedule_id;
  selectedDate.value = date;
  selectedTimeStart.value = start;
  selectedTimeEnd.value = end;
  isModalVisible.value = true;
}

// 确认预约
async function confirmBooking() {
  if (!selectedDoctor.value ||  !selectedschedule.value) {
    message.error('缺少预约信息');
    return;
  }

  let relation = localStorage.getItem('relation');
  try {
    const response = await http.request('/user/appointment/book/', 'POST_JSON',
        {
          schedule_id: selectedschedule.value,
          relation: relation
        }); // 根据实际 API 路径调整

    if (response.data.status === 'success') {
      message.success('预约成功');
      // 刷新数据
      await fetchAppointmentInfo();
    } else {
      message.error(response.data.message || '预约失败');
    }
  } catch (error) {
    message.error('预约失败');
    console.error(error);
  } finally {
    isModalVisible.value = false;
  }
}

// 切换科室的展开状态
function toggleDepartment(departmentIndex: number) {
  // 通过修改 activeDepartmentKeys 来控制展开
  const currentKey = activeDepartmentKeys.value[departmentIndex];
  activeDepartmentKeys.value.splice(departmentIndex, 1, currentKey ? null : departmentIndex.toString());
}

onMounted(() => {
  fetchAppointmentInfo();
});
</script>
<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.view-appointments-button {
  margin-left: auto;
}

.state-cancelled {
  color: red;
}

.state-completed {
  color: green;
}

.state-active {
  color: blue;
}
</style>
<style scoped>

.doctor-details {
  display: flex;
  flex-wrap: wrap;
}

.doctor-info {
  display: flex;
  width: 100%;
}


 .date-title {
   font-size: 2.0em;
   font-weight: bold;
   width: 150px;


   padding: 10px;
   border-radius: 8px;
   text-align: center;


   font-family: 'Courier New', Courier, monospace;
   text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
 }

.doctor-info-left {
  flex: 1;
}

.doctor-info-right {
  flex: 1;
}

.doctor-info p {
  margin: 0;
}

.doctor-introduction {
  margin-top: 8px;
}


.floating-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  min-width: 600px;
  min-height: 200px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 999;
  padding: 20px;
  overflow: hidden;
}

.modal-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.modal-body {
  flex: 1;
  margin-bottom: 20px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-button,
.cancel-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-button {
  background-color: #1890ff;
  color: #fff;
}

.cancel-button {
  background-color: #f0f0f0;
  color: #000;
}

.appointment-schedule {
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

.search-input {
  max-width: 400px;
  margin: 0 auto 20px auto;
  display: block;
}

.department-container {
  margin-bottom: 16px;
}

.department-card {
  padding: 16px 10px 10px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s;
  cursor: auto;
}

.department-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.doctor-container {
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
  margin-top: 8px;
}
.myfooter {
  position: absolute;
  bottom: 20px;
  right: 20px;

}
.doctor-avatar {
  border-radius: 8px;
}


.schedule-times {
  margin-top: 8px;
}

.schedule-times h3 {
  margin-bottom: 8px;
  color: #595959;
}

.time-slot-container {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  background-color: #fafafa;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.myabutton {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  margin-bottom: 8px;
}

.appointment-modal {
  /* 不需要自定义样式，使用Ant Design Vue默认样式确保模态框居中 */
}

.mypanel {

  border-radius: 4px;
  align-content: revert;

  font-weight: lighter;
  font-size: 16px;
  bordered: true;
}

.floating-modal-another {
   position: fixed;
   top: 50%;
   left: 50%;
   transform: translate(-50%, -50%);
   min-width: 800px;
   min-height: 500px;
   background-color: white;
   border-radius: 8px;
   box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
   z-index: 999;
   padding: 20px;
   overflow: hidden;
   cursor: move;

 }

.myhead {
  font-size: 20px;
  font-weight: lighter;
}
@media (max-width: 768px) {
  .schedule-times a-button {
    min-width: 80px;
    margin-bottom: 8px;
  }
}
</style>
<style scoped>
.search-container {
  display: flex;
  align-items: center;
  gap: 550px;
  margin-bottom: 20px;
  margin-right: 40px;
}

.search-input {
  flex: 1;
}

.view-appointments-button {
  margin-left: auto;
}
</style>
<style scoped>
.title {
  text-align: left;
  margin-bottom: 20px;
  margin-left : 20px;
  font-size: 2em;
  color: #1890ff;
}
</style>