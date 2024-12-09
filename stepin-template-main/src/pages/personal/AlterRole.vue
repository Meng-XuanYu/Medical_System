<!-- RoleSwitch.vue -->
<template>
  <div class="role-switch">
    <h1>角色切换</h1>
    <a-card>

      <a-radio-group>
        <a-radio-button
            @click="handleRoleChange(family.relation)"
            v-for="family in familyMembers"
            :key="family.relation"
            :value="family.relation"
            :style="{backgroundColor: family.relation === selectedRole ? '#1a9def' : '' ,height: '50px',textAlign: 'center',lineHeight: '50px'}"

        >
          {{ family.relation }}（{{ family.name }}）
        </a-radio-button>
      </a-radio-group>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';

interface FamilyMember {
  family_id: string;
  relation: string;
  name: string;
}

const familyMembers = ref<FamilyMember[]>([]);
const selectedRole = ref<string>('本人'); // Initialize with type and default value


function fetchFamilyMembers() {
  familyMembers.value = [
    { family_id: '0', relation: '本人', name: '张老师' },
    { family_id: 'F01', relation: '配偶', name: '王女士' },
    { family_id: 'F02', relation: '子女', name: '李小明' },
  ];

  selectedRole.value = localStorage.getItem('relation') || '本人';
}

function handleRoleChange(family: string) {
  localStorage.setItem('relation', family);
  selectedRole.value = family;
  console.log('selectedRole:', family);
}

onMounted(fetchFamilyMembers);


</script>

<style scoped>
.role-switch {
  padding: 24px;
}
</style>
