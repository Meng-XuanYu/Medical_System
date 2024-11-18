<!-- RoleSwitch.vue -->
<template>
  <div class="role-switch">
    <h1>角色切换</h1>
    <a-card>
      <a-radio-group v-model="selectedRole" @change="handleRoleChange">
        <a-radio-button :value="user.id" key="self">
          本人（{{ user.name }}）
        </a-radio-button>
        <a-radio-button v-for="family in familyMembers" :value="family.family_id" :key="family.family_id">
          {{ family.relationship }}（{{ family.name }}）
        </a-radio-button>
      </a-radio-group>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

const user = reactive({
  id: 'T1234567',
  name: localStorage.getItem(),
});

const familyMembers = ref([]);
const selectedRole = ref(user.id);

function fetchFamilyMembers() {
  // 调用后端API获取家属列表
  // axios.get(`/api/familyMembers?teacher_id=${user.id}`).then(response => {
  //   familyMembers.value = response.data;
  // });

  // 模拟数据
  familyMembers.value = [
    {
      family_id: 'F01',
      relationship: '配偶',
      name: '王女士',
    },
    {
      family_id: 'F02',
      relationship: '子女',
      name: '李小明',
    },
  ];
}

function handleRoleChange() {
  // 更新当前身份，影响后续请求的参数
  // 保存 selectedRole.value 到全局状态或本地存储
}

onMounted(() => {
  fetchFamilyMembers();
});
</script>

<style scoped>
.role-switch {
  padding: 24px;
}
</style>
