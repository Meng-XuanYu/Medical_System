<template>
  <div class="container">
    <h1>医生评价系统</h1>
    <div class="doctor-list">
      <div
          class="doctor-card"
          v-for="doctor in doctors"
          :key="doctor.doctor_id"
          @click="openModal(doctor)"
      >

        <img :src="doctor.image_id" :alt="doctor.name" />
        <div class="doctor-info">
          <h3>{{ doctor.name }}</h3>
          <p>{{ doctor.title }}</p>
        </div>
      </div>
    </div>

    <!-- 模态框 -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <span class="close-button" @click="closeModal">&times;</span>
        <div class="doctor-details">
          <img :src="selectedDoctor.image_id" :alt="selectedDoctor.name" />
          <div class="details">
            <h2>{{ selectedDoctor.name }}</h2>
            <p><strong>职称：</strong>{{ selectedDoctor.title }}</p>
            <p><strong>简介：</strong>{{ selectedDoctor.introduction }}</p>
          </div>
        </div>

        <div class="evaluations">
          <h3>用户评价</h3>
          <div v-if="selectedDoctor.evaluations.length === 0">
            <p>暂无评价。</p>
          </div>
          <div v-else>
            <div class="evaluation" v-for="(evaluation, index) in selectedDoctor.evaluations" :key="index">
              <img :src="evaluation.user_image" width="50px"  />
              <p><strong>用户ID:</strong> {{ evaluation.user_id }}</p>
              <p><strong>评价:</strong> {{ evaluation.evaluation }}</p>
              <p><strong>评分:</strong> <span class="stars">{{ renderStars(evaluation.star) }}</span></p>
              <p class="time">{{ evaluation.time }}</p>
            </div>
          </div>
        </div>

        <div class="submit-evaluation">
          <h3>提交你的评价</h3>
          <form @submit.prevent="submitEvaluation">
            <div class="form-group">
              <label for="evaluation">评价内容：</label>
              <textarea id="evaluation" v-model="newEvaluation.evaluation" required></textarea>
            </div>
            <div class="form-group">
              <label for="star">评分：</label>
              <select id="star" v-model.number="newEvaluation.star" required>
                <option disabled value="">请选择星级</option>
                <option v-for="n in 5" :key="n" :value="n">{{ n }} 星</option>
              </select>
            </div>
            <button type="submit">提交评价</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import http from '@/store/http';

export default {
  name: 'DoctorEvaluation',
  setup() {
    const doctors = ref([]);
    const isModalOpen = ref(false);
    const selectedDoctor = ref({});
    const newEvaluation = ref({
      doctor_id: null,
      evaluation: '',
      star: null,
    });

    // 获取医生头像的完整URL
    const getDoctorImageUrl = (imageId) => {
      return `/media/images/${imageId}.jpg`; // 根据你的实际路径调整
    };

    // 渲染星级
    const renderStars = (star) => {
      return '★'.repeat(star) + '☆'.repeat(5 - star);
    };

    // 获取医生及其评价数据
    const fetchDoctors = async () => {
      try {
        const response = await http.request('/user/get_doctors_comments/','get',{});
        doctors.value = response.data.doctors;
      } catch (error) {
        console.error('获取医生数据失败:', error);
        alert('无法获取医生数据，请稍后再试。');
      }
    };

    // 打开模态框并设置选中的医生
    const openModal = (doctor) => {
      selectedDoctor.value = { ...doctor };
      newEvaluation.value = {
        doctor_id: doctor.doctor_id,
        evaluation: '',
        star: null,
      };
      isModalOpen.value = true;
    };

    // 关闭模态框
    const closeModal = () => {
      isModalOpen.value = false;
    };

    // 提交评价
    const submitEvaluation = async () => {
      if (!newEvaluation.value.evaluation || !newEvaluation.value.star) {
        alert('请填写评价内容和评分。');
        return;
      }

      try {
        const response = await http.request('/user/comment/', 'POST_JSON', {
              doctor_id: newEvaluation.value.doctor_id,
              evaluation: newEvaluation.value.evaluation,
              star: newEvaluation.value.star,
            });

        // 将新评价添加到当前医生的评价列表
        selectedDoctor.value.evaluations.push(response.data);


        // 重置评价表单
        newEvaluation.value.evaluation = '';
        newEvaluation.value.star = null;

        alert('评价提交成功！');
      } catch (error) {
        console.error('提交评价失败:', error);
        if (error.response && error.response.data && error.response.data.message) {
          alert(`提交失败: ${error.response.data.message}`);
        } else {
          alert('提交评价失败，请稍后再试。');
        }
      }
    };

    // 获取CSRF Token（假设你使用Django的默认CSRF保护）
    const getCookie = (name) => {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    };

    onMounted(() => {
      fetchDoctors();
    });

    return {
      doctors,
      isModalOpen,
      selectedDoctor,
      newEvaluation,
      openModal,
      closeModal,
      submitEvaluation,
      getDoctorImageUrl,
      renderStars,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 40px;
}

.doctor-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.doctor-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  width: 200px;
  cursor: pointer;
  transition: transform 0.2s;
}

.doctor-card:hover {
  transform: translateY(-5px);
}

.doctor-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.doctor-info {
  padding: 15px;
  text-align: center;
}

.doctor-info h3 {
  margin: 10px 0 5px;
  font-size: 1.2em;
}

.doctor-info p {
  margin: 0;
  color: #666;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  width: 90%;
  max-width: 800px;
  border-radius: 8px;
  padding: 20px;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.close-button {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
}

.close-button:hover {
  color: #ff0000;
}

.doctor-details {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.doctor-details img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.details {
  flex: 1;
}

.evaluations {
  margin-bottom: 20px;
}

.evaluation {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.evaluation:last-child {
  border-bottom: none;
}

.evaluation p {
  margin: 5px 0;
}

.stars {
  color: gold;
}

.time {
  color: #999;
  font-size: 0.9em;
}

.submit-evaluation {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
  height: 100px;
}

button[type='submit'] {
  background-color: #28a745;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type='submit']:hover {
  background-color: #218838;
}
</style>
