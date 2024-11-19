<template>
  <div class="appointment-schedule">
    <h1 class="title">预约排班信息</h1>
    <a-input-search
        v-model="searchText"
        placeholder="请输入科室名称、医生姓名"
        @search="fetchAppointmentInfo"
        enter-button
        class="search-input"
        allow-clear
    />
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
            <hr/>
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
                        :src="getImagePath(doctor.image_id)"
                        width="160"
                        class="doctor-avatar"
                    />
                  </a-col>
                  <a-col :span="20">
                    <div class="doctor-details">
                      <p><strong>姓名：</strong>{{ doctor.name }}</p>
                      <p><strong>性别：</strong>{{ doctor.gender }}</p>
                      <p><strong>职称：</strong>{{ doctor.title }}</p>
                    </div>
                    <div class="schedule-times">
                      <h3>可预约时间段：</h3>
                      <a-row :gutter="[8, 8]">
                        <a-col
                            v-for="(timeSlot, timeIndex) in groupedScheduleTimes(doctor.schedule_times)"
                            :key="timeIndex"
                            :span="24"
                        >
                          <h4>{{ timeSlot.date }}</h4>
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
                        </a-col>
                      </a-row>
                    </div>
                  </a-col>
                </a-row>
              </a-collapse-panel>
            </a-collapse>
          </a-card>
        </a-col>
      </a-row>
    </a-spin>
    <a-modal ref="modalRef"
             v-model:visible="isModalVisible"
             title="预约确认"
             :wrap-style="{ overflow: 'hidden' }"
             @ok="confirmBooking"
             @cancel="isModalVisible = false"
             ok-text="确认"
             cancel-text="取消"
    >
      <p>
        你确定要预约 <strong>{{ selectedDoctor.name }}</strong> 在
        <strong>{{ selectedDate }}</strong> {{ formatTime(selectedTimeStart) }} - {{ formatTime(selectedTimeEnd) }}
        进行问诊吗？
      </p>
      <template #modalRender="{ originVNode }">
        <div :style="transformStyle">
          <component :is="originVNode"/>
        </div>
      </template>
    </a-modal>

  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
import {message} from 'ant-design-vue';
import {CalendarOutlined} from '@ant-design/icons-vue';
import http from '@/store/http';

import {computed, CSSProperties, watch, watchEffect} from 'vue';
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
    appointmentData.value = response.data;
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

// 获取图片路径
function getImagePath(image_id: string): string {
  return 'src/assets/' + image_id + '.jpg'; // 根据实际路径调整
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

    if (response.data.success) {
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

.doctor-avatar {
  border-radius: 8px;
}

.doctor-details {
  margin-bottom: 8px;
}

.schedule-times {
  margin-top: 8px;
}

.schedule-times h3 {
  margin-bottom: 8px;
  color: #595959;
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

  font-weight: bolder;
  font-size: 16px;
  bordered: true;
}

.myhead {
  font-size: 20px;
  font-weight: bold;
}
@media (max-width: 768px) {
  .schedule-times a-button {
    min-width: 80px;
    margin-bottom: 8px;
  }
}
</style>
