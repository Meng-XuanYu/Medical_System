<!-- RoleSwitch.vue -->
<template>
  <div class="role-switch">
    <h1>角色切换</h1>
    <a-card>
      <a-radio-group v-model="selectedRole" @change="handleRoleChange">
        <a-radio-button
            v-for="family in familyMembers"
            :value="family.family_id"
            :key="family.family_id"
            :style="{ color: family.relation === currentRelation ? 'blue' : '' }"
        >
          {{ family.relation }}（{{ family.name }}）
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
  name: '本人'
});

const familyMembers = ref([]);
const selectedRole = ref(user.id);
const currentRelation = ref(localStorage.getItem('relation') || '本人');

function fetchFamilyMembers() {
  // 模拟数据
  familyMembers.value = [
    {
      family_id: '0',
      relation: '本人',
      name: '张老师',
    },
    {
      family_id: 'F01',
      relation: '配偶',
      name: '王女士',
    },
    {
      family_id: 'F02',
      relation: '子女',
      name: '李小明',
    },
  ];

  const storedRelation = localStorage.getItem('relation');

  if (storedRelation) {
    const family = familyMembers.value.find(f => f.relation === storedRelation);
    if (family) {
      selectedRole.value = family.family_id;
    } else {
      selectedRole.value = user.id;
    }
  } else {
    selectedRole.value = user.id; // 默认选中本人
  }
}

function handleRoleChange() {
  const family = familyMembers.value.find(f => f.family_id === selectedRole.value);
  if (family) {
    currentRelation.value = family.relation;
    localStorage.setItem('relation', family.relation);
  } else {
    currentRelation.value = '本人';
    localStorage.setItem('relation', '本人');
  }
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

